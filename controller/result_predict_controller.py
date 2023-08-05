import json

from flask import Response, request

from controller import app, API_ROOT, get_message_by_request
from service.ResultPredictService import ResultPredictService
from utils import logging_helpers

logger = logging_helpers.get_custom_logger(name_logging='api')


@app.route(API_ROOT + 'categorical/all/')
def getAllCategorical():
    print('11111111111111')
    s = ResultPredictService(1)
    res = s.getAll()
    logger.debug(get_message_by_request(request))
    return Response(json.dumps(res, ensure_ascii=False), status=200, headers={'Content-Type': 'application/json'})


@app.route(API_ROOT + 'categorical/all_not_null/')
def getAllCategoricalNotNull():
    s = ResultPredictService(1)
    res = s.getAllNotNull()
    logger.debug(get_message_by_request(request))
    return Response(json.dumps(res, ensure_ascii=False), status=200, headers={'Content-Type': 'application/json'})
