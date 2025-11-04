import importlib
import inspect

from functools import lru_cache
from typing import Any, TypeVar

from backend.common.exception import errors
from backend.common.log import log

T = TypeVar('T')


@lru_cache(maxsize=512)
def import_module_cached(module_path: str) -> Any:
    """
    Cached module import

    :param module_path: Module path
    :return:
    """
    return importlib.import_module(module_path)


def dynamic_import_data_model(module_path: str) -> type[T]:
    """
    Dynamically import data model

    :param module_path: Module path, format is 'module_path.class_name'
    :return:
    """
    try:
        module_path, class_name = module_path.rsplit('.', 1)
        module = import_module_cached(module_path)
        return getattr(module, class_name)
    except Exception as e:
        log.error(f'Failed to dynamically import data model: {e}')
        raise errors.ServerError(msg='Failed to dynamically parse data model, please contact system administrator')


def get_model_objects(module_path: str) -> list[type] | None:
    """
    Get model objects

    :param module_path: Module path
    :return:
    """
    try:
        module = import_module_cached(module_path)
    except ModuleNotFoundError:
        log.warning(f'Module {module_path} does not contain model objects')
        return None
    except Exception:
        raise

    classes = []

    for _name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and module_path in obj.__module__:
            classes.append(obj)

    return classes
