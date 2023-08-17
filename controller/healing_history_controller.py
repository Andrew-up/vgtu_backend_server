import json

from flask import request, Response

from controller import app, API_ROOT, get_message_by_request
from service.HealingHistoryService import HealingHistoryService
from service.patientService import PatientService
from utils import logging_helpers

logger = logging_helpers.get_custom_logger(name_logging='api')


@app.route(API_ROOT + 'patient/history/<id_patient>/')
def get_all_history_by_patient_id(id_patient):

    """
    :param REQUEST: HTTP запрос (GET)
    :param int id_patient: - id пациента
    :return: список историй лечения одного пациента

    Пример::

        'GET http://localhost:8080/api/patient/history/1/'

        Ответ:
        [
           {
              "history_neural_network_id":1,
              "patient_id":1,
              "comment":"тест",
              "date":"2023-08-15 13:20:37.230415",
              "id_healing_history":1,
              "history_neutral_network":{
                 "photo_original":"base64 image",
                 "photo_predict":"base64 image",
                 "photo_predict_edit_doctor":"base64 image",
                 "id_history_neural_network":3,
                 "annotations":[
                    {
                       "segmentation":"[178.0, 294.0, 193.0, 236.0, 247.0, 263.0, 261.0, 319.0, 211.0, 320.0, 178.0, 294.0]",
                       "category_id":2,
                       "area":4584.0,
                       "id_annotations":3,
                       "bbox":"[178, 236, 84, 85]",
                       "history_nn_id":3,
                       "result_predict":{
                          "name_category_eng":"cat1_2",
                          "id_category":2,
                          "color":"(0, 0, 255)",
                          "name_category_ru":"Асептическое 2 стадия"
                       }
                    },
                    {
                       "segmentation":"[313.0, 362.0, 327.0, 299.0, 356.0, 318.0, 345.0, 360.0, 313.0, 362.0]",
                       "category_id":2,
                       "area":1707.5,
                       "id_annotations":4,
                       "bbox":"[313, 299, 44, 64]",
                       "history_nn_id":3,
                       "result_predict":{
                          "name_category_eng":"cat1_2",
                          "id_category":2,
                          "color":"(0, 0, 255)",
                          "name_category_ru":"Асептическое 2 стадия"
                       }
                    }
                 ]
              }
           }
        ]


    """
    logger.debug(get_message_by_request(request))
    s = HealingHistoryService(1)
    res = s.getAllHistoryByIdPatient(id_patient=id_patient)
    res2 = [p.to_dict() for p in res]
    return Response(json.dumps(res2, ensure_ascii=False), status=200,
                    headers={'Content-Type': 'application/json'})


@app.route(API_ROOT + 'history/add/<id_patient>/', methods=['POST'])
def add_history_patient(id_patient):
    """
    :param REQUEST: HTTP запрос (POST)
    :param int id_patient: id пациента, в данный момент не используется
    :return: 'История добавлена'

    Пример::

        POST http://localhost:8080/api/history/add/1/

        тело:
        {
           "patient_id":1,
           "history_neutral_network":{
              "id_history_neural_network":0,
              "photo_original":"b'iVBORw0KGgoAAAANSUh'",
              "photo_predict":"b'iVBORw0KGgoAAAANSUh'",
              "photo_predict_edit_doctor":"b'iVBORw0KGgoAAAANSUh'",
              "healing_history_id":0,
              "annotations":[
                 {
                    "id_annotations":1,
                    "area":5230.5,
                    "bbox":[
                       91,
                       235,
                       142,
                       82
                    ],
                    "segmentation":[
                       91.0,
                       316.0,
                       121.0,
                       235.0,
                       232.0,
                       284.0,
                       91.0,
                       316.0
                    ],
                    "history_nn_id":"None",
                    "category_id":7,
                    "category":{
                       "id_category":7,
                       "name_category_eng":"cat3_1",
                       "name_category_ru":"Гнойное 1 стадия",
                       "color":"(255, 0, 0)"
                    }
                 }
              ]
           },
           "patient":"None",
           "doctor":"None",
           "comment":"тест",
           "date":"2023-08-09 11:22:28.510759"
        }

        Ответ:

            'История добавлена'

    """
    logger.debug(get_message_by_request(request))
    service = PatientService(1)
    service.addHealingHistoryPatient(request.json)
    return Response('История добавлена', status=200)



# @app.route(API_ROOT + 'history/<id_history>/')
# def get_history_by_history_id(id_history):
#     logger.debug(get_message_by_request(request))
#     s = HealingHistoryService(1)
#     h = healingHistoryDTO.HealingHistoryDTO(**HealingHistory().__dict__).getDto().__dict__
#     res: HealingHistory = s.getHistoryById(id_history)
#     if res is not None:
#         h: healingHistoryDTO.HealingHistoryDTO = healingHistoryDTO.HealingHistoryDTO(**res.__dict__).getDto().__dict__
#     return Response(json.dumps(h, ensure_ascii=False), status=200,
#                     headers={'Content-Type': 'application/json'})
