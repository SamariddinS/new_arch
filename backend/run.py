import os

import uvicorn

if __name__ == '__main__':
    # Why this separate startup file: https://stackoverflow.com/questions/64003384

    # DEBUG:
    # If you prefer to DEBUG in IDE, you can directly right-click to start this file in IDE
    # If you prefer to debug using print, it is recommended to use fba cli to start the service

    # Warning:
    # If you are starting this file via python command, please follow these guidelines:
    # 1. Install dependencies via uv according to the official documentation
    # 2. Command line workspace should be in the backend directory
    uvicorn.run(
        app='backend.main:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
        reload_excludes=[os.path.abspath('../.venv')],
    )
