import json

from flask import Response, request

from controller import app, API_ROOT, get_message_by_request
from service.ResultPredictService import ResultPredictService
from utils import logging_helpers

logger = logging_helpers.get_custom_logger(name_logging='api')


@app.route(API_ROOT + 'categorical/all/')
def getAllCategorical():
    s = ResultPredictService(1)
    res = json.dumps(
        [ob.to_dict(only=('id_category', 'color', 'name_category_ru', 'name_category_eng')) for ob in s.getAll()],
        ensure_ascii=False)

    logger.debug(get_message_by_request(request))

    return Response(res, status=200, headers={'Content-Type': 'application/json'})

# @app.route(API_ROOT + 'categorical/all_not_null/')
# def getAllCategoricalNotNull():
#     s = ResultPredictService(1)
#     res = s.getAllNotNull()
#     logger.debug(get_message_by_request(request))
#     return Response(json.dumps(res, ensure_ascii=False), status=200, headers={'Content-Type': 'application/json'})
