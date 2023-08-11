import json

from flask import request, Response

from controller import app, API_ROOT, get_message_by_request
from definitions import SECRET_KEY, CONTENT_TYPE_JSON
from service.patientService import PatientService
from utils import logging_helpers

logger = logging_helpers.get_custom_logger(name_logging='api')


@app.route(API_ROOT + "/all/")
def get_patients():
    logger.debug(get_message_by_request(request))
    p = PatientService(1)
    json_string = json.dumps([ob.to_dict() for ob in p.getAll()], ensure_ascii=False)
    return Response(json_string, content_type=CONTENT_TYPE_JSON)


@app.route(API_ROOT + 'patient/<id>/')
def get_patient_by_id(id):
    logger.debug(get_message_by_request(request))
    s_service = PatientService(1)
    p = s_service.getById(id)
    return Response(json.dumps(p.to_dict(), ensure_ascii=False), status=200, content_type=CONTENT_TYPE_JSON)


@app.route(API_ROOT + "/add/", methods=['POST'])
def add_new_patient():
    logger.debug(get_message_by_request(request))
    s_service = PatientService(1)
    res = s_service.add(request.json)
    json_string = json.dumps(res.to_dict(), ensure_ascii=False)
    return Response(json_string, 200, content_type=CONTENT_TYPE_JSON)


@app.route(API_ROOT + 'patient/delete/<id>', methods=['POST', 'GET'])
def delete_patient(id):
    if request.method == 'POST':
        r = request.json
        if r['key'] == SECRET_KEY:
            print('delete')
            service = PatientService(1)
            res = service.deletePatientById(id_patient=id)
            logger.debug(get_message_by_request(request))
            return Response(res, 200)
    else:
        logger.warning(get_message_by_request(request))
        return Response('Ошибка доступа', 401)
