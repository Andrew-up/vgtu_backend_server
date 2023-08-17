import json

from flask import request, Response

from controller import app, API_ROOT, get_message_by_request
from definitions import SECRET_KEY, CONTENT_TYPE_JSON
from service.patientService import PatientService
from utils import logging_helpers

logger = logging_helpers.get_custom_logger(name_logging='api')


@app.route(API_ROOT + "/all/")
def get_patients():

    """
    :param REQUEST: HTTP запрос (GET)
    :return: Список пациентов в формате JSON

    Пример::

        >>> 'GET http://localhost:8080/api/all/'

        [
            {
                "surname": "Баранов",
                "date_of_birth": "1997-03-08",
                "gender": "male",
                "phone": "+7(985)-965-30-29",
                "id_patient": 1,
                "snils": "136-656-636-56",
                "date_healing_start": null,
                "polis_oms": "7167 8929 3340 2891",
                "dianosis": null,
                "date_healing_end": null,
                "firstname": "Вадим",
                "address": "г.Воронеж ул. Волгоградская дом. 49 кв. 105",
                "middlename": "Михайлович",
                "document": "Паспорт серия: 12 14 №:308959"
            },
            {
                "surname": "Павлов",
                "date_of_birth": "1996-01-22",
                "gender": "male",
                "phone": "+7(976)-545-63-95",
                "id_patient": 2,
                "snils": "939-627-637-52",
                "date_healing_start": null,
                "polis_oms": "4293 8977 9400 4169",
                "dianosis": null,
                "date_healing_end": null,
                "firstname": "Антон",
                "address": "г.Воронеж ул. Антонова-Овсиенко дом. 69 кв. 91",
                "middlename": "Дмитриевич",
                "document": "Паспорт серия: 16 17 №:233470"
            }
        ]

    """

    logger.debug(get_message_by_request(request))
    p = PatientService(1)
    json_string = json.dumps([ob.to_dict() for ob in p.getAll()], ensure_ascii=False)
    return Response(json_string, content_type=CONTENT_TYPE_JSON)


@app.route(API_ROOT + 'patient/<id>/')
def get_patient_by_id(id):
    """
        :param REQUEST: HTTP запрос (GET)
        :param int id: id пациента
        :return: Пациента в формате JSON

        Пример::

            >>> 'GET http://localhost:8080/api/patient/1/'

            {
                "surname": "Баранов",
                "date_of_birth": "1997-03-08",
                "gender": "male",
                "phone": "+7(985)-965-30-29",
                "id_patient": 1,
                "snils": "136-656-636-56",
                "date_healing_start": null,
                "polis_oms": "7167 8929 3340 2891",
                "dianosis": null,
                "date_healing_end": null,
                "firstname": "Вадим",
                "address": "г.Воронеж ул. Волгоградская дом. 49 кв. 105",
                "middlename": "Михайлович",
                "document": "Паспорт серия: 12 14 №:308959"
            }

        """

    logger.debug(get_message_by_request(request))
    s_service = PatientService(1)
    p = s_service.getById(id)
    return Response(json.dumps(p.to_dict(), ensure_ascii=False), status=200, content_type=CONTENT_TYPE_JSON)


@app.route(API_ROOT + "/add/", methods=['POST'])
def add_new_patient():

    """
    :param: Принимает JSON в POST запросе см. пример.
    :return: JSON Пациент

    Пример::

        >>> 'POST http://localhost:8080/api/add/'

        Тело:

            {
               "date_of_birth":"1972-12-01",
               "date_healing_start":"None",
               "phone":"+7(950)-576-58-15",
               "polis_oms":"4525 3053 7147 9661",
               "dianosis":"None",
               "date_healing_end":"None",
               "address":"г.Воронеж ул. Бульвар Победы дом. 26 кв. 113",
               "gender":"male",
               "document":"Паспорт серия: 18 16 №:518977",
               "snils":"375-149-798-65",
               "middlename":"Михайлович",
               "firstname":"Дмитрий",
               "surname":"Михайлов"
            }

    """
    logger.debug(get_message_by_request(request))
    s_service = PatientService(1)
    res = s_service.add(request.json)
    json_string = json.dumps(res.to_dict(), ensure_ascii=False)
    return Response(json_string, 200, content_type=CONTENT_TYPE_JSON)


@app.route(API_ROOT + 'patient/delete/<id>', methods=['POST', 'GET'])
def delete_patient(id):

    """

    В теле запроса нужно передать JSON который содержит значение
    ``{"key":"SECRET_KEY"}``

    :param id: Удаляет пациента по ID
    :return: status 200 Если успешно или 401 если ошибка

    Пример::

        POST http://localhost:8080/api/patient/delete/1
        Тело: {"key":"SECRET_KEY"}

        Ответ: Удаление успешно

        GET http://localhost:8080/api/patient/delete/1

        Ответ: Ошибка доступа


    """
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
