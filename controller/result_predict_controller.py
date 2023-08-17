import json

from flask import Response, request

from controller import app, API_ROOT, get_message_by_request
from service.ResultPredictService import ResultPredictService
from utils import logging_helpers

logger = logging_helpers.get_custom_logger(name_logging='api')


@app.route(API_ROOT + 'categorical/all/')
def get_all_categorical():

    """
    :return: Cписок категорий для предсказания нейронной сетью

    Пример::

        >>> 'GET http://localhost:8080/api/categorical/all/'

        Ответ:
        [
            {
                "name_category_ru": "Асептическое",
                "id_category": 1,
                "name_category_eng": "cat1_1",
                "color": "(255, 0, 0)"
            },
            {
                "name_category_ru": "Бактериальное",
                "id_category": 2,
                "name_category_eng": "cat1_2",
                "color": "(0, 255, 0)"
            },
            {
                "name_category_ru": "Гнойное",
                "id_category": 3,
                "name_category_eng": "cat1_3",
                "color": "(0, 0, 255)"
            }
        ]


    """
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
