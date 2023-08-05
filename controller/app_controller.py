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
    logger.debug(get_message_by_request(request))
    # print()
    return ReadXmlProject().app_version


@app.route('/api/app/status/')
def check_status_server():
    logger.debug(get_message_by_request(request))
    return Response(json.dumps({'status': 'ok'}))


@app.route('/api/app/update/download/')
def download():
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
