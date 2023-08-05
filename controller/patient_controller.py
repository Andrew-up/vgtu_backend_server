import json

from flask import request, Response

from controller import app, API_ROOT, get_message_by_request
from definitions import SECRET_KEY
from dto.patientDTO import PatientDTO
from service.patientService import PatientService
from utils import logging_helpers

logger = logging_helpers.get_custom_logger(name_logging='api')


@app.route(API_ROOT + "/all/")
def get_patients():
    logger.debug(get_message_by_request(request))
    p = PatientService(1)
    zzz = p.getAll()
    json_string = json.dumps([ob.__dict__ for ob in zzz], ensure_ascii=False)
    return json_string


@app.route(API_ROOT + 'patient/<id>/')
def get_patient_by_id(id):
    logger.debug(get_message_by_request(request))
    s_service = PatientService(1)
    p = s_service.getById(id)
    json_string = json.dumps(p.__dict__, ensure_ascii=False)
    return Response(json_string, status=200)


@app.route(API_ROOT + "/add/", methods=['POST'])
def add_new_patient():
    logger.debug(get_message_by_request(request))
    data1: PatientDTO.__dict__ = request.json
    dto = PatientDTO(**data1)
    s_service = PatientService(1)
    res = s_service.add(dto)
    json_string = json.dumps(res.__dict__, ensure_ascii=False)
    return Response(json_string, 200)


@app.route(API_ROOT + 'patient/delete/<id>', methods=['POST', 'GET'])
def delete_patient(id):
    if request.method == 'POST':
        r = request.json
        if r['key'] == SECRET_KEY:
            print('delete')
            srvise = PatientService(1)
            res = srvise.deletePatientById(id_patient=id)
            logger.debug(get_message_by_request(request))
            return Response(res, 200)
    else:
        logger.warning(get_message_by_request(request))
        return Response('Ошибка доступа', 401)
