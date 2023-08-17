"""


Описание:


HTTP контроллер для приложения, не взаимодействует с БД
Может выдать версию приложения, статус сервера, файлы для обновления и т.д

"""

import json
import os

from flask import Response, stream_with_context, request

from controller import app, read_file_chunks, get_message_by_request
from definitions import RELEASE_DIR
from utils import logging_helpers
from utils.read_xml_file import ReadXmlProject

logger = logging_helpers.get_custom_logger(name_logging='api')



@app.route('/api/app/version/')
def check_version():
    """




    :param REQUEST: HTTP запрос (GET)

    Позволяет получить версию проекта, прочивав xml file project.xml

    Пример::

        >>> 'GET http://localhost:8080/api/app/version/'
        "1.0.0"

    """
    logger.debug(get_message_by_request(request))
    return ReadXmlProject().app_version


@app.route('/api/app/status/')
def check_status_server():
    """
    :param REQUEST: HTTP запрос (GET)

    Позволяет получить статус сервера, если он включен то возращает JSON

    Пример::

        >>> 'GET http://localhost:8080/api/app/status/'
        {'status': 'ok'}

    """
    logger.debug(get_message_by_request(request))
    return Response(json.dumps({'status': 'ok'}))




@app.route('/api/app/update/download/')
def download():
    """


    :param REQUEST: HTTP запрос (GET)

    Ищет файл **Release.zip** в директории **root/Release/**

    - Если файл найден, то возвращает его.
    - Если файла нет, возвращает JSON.

    Пример::

        >>> 'GET http://localhost:8080/api/app/update/download/'

        {
            "error:": "Файл обновлений не доступен для загрузки"
        }

    """

    zip_file_path = os.path.join(RELEASE_DIR, 'Release.zip')
    logger.debug(get_message_by_request(request))
    if os.path.exists(zip_file_path):
        stats = os.stat(zip_file_path)
        return Response(
            stream_with_context(read_file_chunks(zip_file_path)),
            headers={
                'Content-Length': f'{stats.st_size}',
                'Content-Disposition': f'attachment; filename=Release.zip'
            })
    else:
        logger.warning(get_message_by_request(request))
        return Response(json.dumps({'error:': f'Файл обновлений не доступен для загрузки'}, ensure_ascii=False))
