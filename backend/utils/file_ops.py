import io
import os
import re
import zipfile

import anyio

from anyio import open_file
from dulwich import porcelain
from fastapi import UploadFile
from sqlparse import split

from backend.common.enums import FileType
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR, UPLOAD_DIR
from backend.database.redis import redis_client
from backend.plugin.tools import install_requirements_async
from backend.utils.re_verify import is_git_url
from backend.utils.timezone import timezone


def build_filename(file: UploadFile) -> str:
    """
    Build filename

    :param file: FastAPI upload file object
    :return:
    """
    timestamp = int(timezone.now().timestamp())
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    new_filename = f'{filename.replace(f".{file_ext}", f"_{timestamp}")}.{file_ext}'
    return new_filename


def upload_file_verify(file: UploadFile) -> None:
    """
    File verification

    :param file: FastAPI upload file object
    :return:
    """
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    if not file_ext:
        raise errors.RequestError(msg='Unknown file type')

    if file_ext == FileType.image:
        if file_ext not in settings.UPLOAD_IMAGE_EXT_INCLUDE:
            raise errors.RequestError(msg='This image format is not supported')
        if file.size > settings.UPLOAD_IMAGE_SIZE_MAX:
            raise errors.RequestError(msg='Image exceeds maximum size limit, please select another')
    elif file_ext == FileType.video:
        if file_ext not in settings.UPLOAD_VIDEO_EXT_INCLUDE:
            raise errors.RequestError(msg='This video format is not supported')
        if file.size > settings.UPLOAD_VIDEO_SIZE_MAX:
            raise errors.RequestError(msg='Video exceeds maximum size limit, please select another')


async def upload_file(file: UploadFile) -> str:
    """
    Upload file

    :param file: FastAPI upload file object
    :return:
    """
    filename = build_filename(file)
    try:
        async with await open_file(UPLOAD_DIR / filename, mode='wb') as fb:
            while True:
                content = await file.read(settings.UPLOAD_READ_SIZE)
                if not content:
                    break
                await fb.write(content)
    except Exception as e:
        log.error(f'Failed to upload file {filename}: {e!s}')
        raise errors.RequestError(msg='Failed to upload file')
    await file.close()
    return filename


async def install_zip_plugin(file: UploadFile | str) -> str:
    """
    Install ZIP plugin

    :param file: FastAPI upload file object or full file path
    :return:
    """
    if isinstance(file, str):
        async with await open_file(file, mode='rb') as fb:
            contents = await fb.read()
    else:
        contents = await file.read()
    file_bytes = io.BytesIO(contents)
    if not zipfile.is_zipfile(file_bytes):
        raise errors.RequestError(msg='Invalid plugin archive format')
    with zipfile.ZipFile(file_bytes) as zf:
        # Validate archive
        plugin_namelist = zf.namelist()
        plugin_dir_name = plugin_namelist[0].split('/')[0]
        if not plugin_namelist:
            raise errors.RequestError(msg='Invalid plugin archive content')
        if (
            len(plugin_namelist) <= 3
            or f'{plugin_dir_name}/plugin.toml' not in plugin_namelist
            or f'{plugin_dir_name}/README.md' not in plugin_namelist
        ):
            raise errors.RequestError(msg='Plugin archive is missing required files')

        # Check if plugin can be installed
        plugin_name = re.match(
            r'^([a-zA-Z0-9_]+)',
            file.split(os.sep)[-1].split('.')[0].strip()
            if isinstance(file, str)
            else file.filename.split('.')[0].strip(),
        ).group()
        full_plugin_path = anyio.Path(PLUGIN_DIR / plugin_name)
        if await full_plugin_path.exists():
            raise errors.ConflictError(msg='This plugin is already installed')
        await full_plugin_path.mkdir(parents=True, exist_ok=True)

        # Extract (install)
        members = []
        for member in zf.infolist():
            if member.filename.startswith(plugin_dir_name):
                new_filename = member.filename.replace(plugin_dir_name, '')
                if new_filename:
                    member.filename = new_filename
                    members.append(member)
        zf.extractall(full_plugin_path, members)

    await install_requirements_async(plugin_dir_name)
    await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'ture')

    return plugin_name


async def install_git_plugin(repo_url: str) -> str:
    """
    Install Git plugin

    :param repo_url:
    :return:
    """
    match = is_git_url(repo_url)
    if not match:
        raise errors.RequestError(msg='Invalid Git repository URL format')
    repo_name = match.group('repo')
    path = anyio.Path(PLUGIN_DIR / repo_name)
    if await path.exists():
        raise errors.ConflictError(msg=f'{repo_name} plugin is already installed')
    try:
        porcelain.clone(repo_url, PLUGIN_DIR / repo_name, checkout=True)
    except Exception as e:
        log.error(f'Plugin installation failed: {e}')
        raise errors.ServerError(msg='Plugin installation failed, please try again later') from e

    await install_requirements_async(repo_name)
    await redis_client.set(f'{settings.PLUGIN_REDIS_PREFIX}:changed', 'ture')

    return repo_name


async def parse_sql_script(filepath: str) -> list[str]:
    """
    Parse SQL script

    :param filepath: Script file path
    :return:
    """
    path = anyio.Path(filepath)
    if not await path.exists():
        raise errors.NotFoundError(msg='SQL script file does not exist')

    async with await open_file(filepath, encoding='utf-8') as f:
        contents = await f.read(1024)
        while additional_contents := await f.read(1024):
            contents += additional_contents

    statements = split(contents)
    for statement in statements:
        if not any(statement.lower().startswith(_) for _ in ['select', 'insert']):
            raise errors.RequestError(msg='SQL script file contains illegal operations, only SELECT and INSERT are allowed')

    return statements
