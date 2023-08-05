import json

from flask import request, Response

from controller import app, API_ROOT, get_message_by_request
from dto import healingHistoryDTO
from model.model import HealingHistory
from service.HealingHistoryService import HealingHistoryService
from service.patientService import PatientService
from utils import logging_helpers

logger = logging_helpers.get_custom_logger(name_logging='api')


@app.route(API_ROOT + 'patient/history/<id_patient>/')
def getAllHistoryByPatientId(id_patient):
    logger.debug(get_message_by_request(request))
    s = HealingHistoryService(1)
    res: list[HealingHistory] = s.getAllHistoryByIdPatient(id_patient=id_patient)
    json_string = []
    for i in res:
        h: healingHistoryDTO.HealingHistoryDTO = healingHistoryDTO.HealingHistoryDTO(**i.__dict__).getDto()
        json_string.append(h.__dict__)
    # print(json_string)
    return Response(json.dumps(json_string, ensure_ascii=False), status=200,
                    headers={'Content-Type': 'application/json'})


@app.route(API_ROOT + 'history/add/<id_patient>/', methods=['POST'])
def add_history_patient(id_patient):
    logger.debug(get_message_by_request(request))
    data: HealingHistory.__dict__ = request.json
    history = healingHistoryDTO.HealingHistoryDTO(**data).getHealingHistory()
    service = PatientService(1)
    service.addHealingHistoryPatient(history)
    return Response('История добавлена', status=200)


@app.route(API_ROOT + 'history/<id_history>/')
def get_history_by_history_id(id_history):
    logger.debug(get_message_by_request(request))
    s = HealingHistoryService(1)
    h = healingHistoryDTO.HealingHistoryDTO(**HealingHistory().__dict__).getDto().__dict__
    res: HealingHistory = s.getHistoryById(id_history)
    if res is not None:
        h: healingHistoryDTO.HealingHistoryDTO = healingHistoryDTO.HealingHistoryDTO(**res.__dict__).getDto().__dict__
    return Response(json.dumps(h, ensure_ascii=False), status=200,
                    headers={'Content-Type': 'application/json'})
