import json
import os

from flask import Response, request, stream_with_context

from Hgjhgjhgjk import MyClass
from controller import app, API_ROOT, read_file_chunks, get_message_by_request
from model.model import ModelUnet
from repository.ModelUnetRepository import ModelUnetRepository
from utils import logging_helpers
from utils.GenerateCocoJsonFromDataBase import GenerateJsonFileFromDB, CocoJsonFormatClass
from utils.read_xml_file import ReadXmlProject

logger = logging_helpers.get_custom_logger(name_logging='api')


@app.route(API_ROOT + '/model_cnn/last_model/')
def get_last_history():
    logger.debug(get_message_by_request(request))
    r = ModelUnetRepository(1)
    void_history = ModelUnet()
    data = r.get_last_history_train()
    print('data: ')
    print(data.to_dict())
    if data.id:
        data = data.to_dict()
        return Response(json.dumps(data, ensure_ascii=False), status=200,
                        headers={'Content-Type': 'application/json'})
    return Response(json.dumps(void_history.to_dict(), ensure_ascii=False), status=200,
                    headers={'Content-Type': 'application/json'})


@app.route(API_ROOT + '/model_cnn/last_model/download/')
def get_last_history_download():
    version = request.args.get('version')
    logger.debug(get_message_by_request(request))
    if not version:
        return 'Укажите версию для загрузки'
    r = ModelUnetRepository(1)
    data = r.get_history_by_version(version)
    r = ReadXmlProject()
    if data:
        full_path = os.path.join(r.path_train_model + r.model_path, data.name_file)
        zip_name = f'{os.path.splitext(full_path)[0]}.zip'
        stats = os.stat(zip_name)
        print(stats.st_size)
        return Response(
            stream_with_context(read_file_chunks(zip_name)),
            headers={
                'Content-Length': f'{stats.st_size}',
                'Content-Disposition': f'attachment; filename={os.path.splitext(data.name_file)[0]}.zip'
            })
    return 'ok'


def generate_new_version(version: str = None):
    version_str = '1.0.0'
    print(version)
    print('SSSSSSSSSSSSSSSSSSSSS')
    if version is not None:
        n_version = list(version)
        if int(n_version[-1]) <= 99:
            n_version[-1] = str(int(n_version[-1]) + 1)
        if int(n_version[-1]) > 99:
            n_version[-1] = '0'
            n_version[2] = str(int(n_version[2]) + 1)
        if int(n_version[2]) > 99:
            n_version[2] = '0'
            n_version[0] = str(int(n_version[0]) + 1)

        version_str = ''.join(n_version)
    return version_str


@app.route(API_ROOT + '/model_cnn/train/')
def train_model():
    logger.debug(get_message_by_request(request))
    # dto = ModelUnetDTO()
    r = ModelUnetRepository(1)
    data = r.get_last_history_train()
    if data.version is None or data.status == 'completed':
        m = ModelUnet()
        m.status = 'Начат процесс обучения'
        if data:
            m.version = data.version
        m.version = generate_new_version(m.version)
        m.name_file = f'model_{m.version.replace(".", "_")}.pth'
        m.path_dataset = str(m.version.replace(".", "_"))
        new_data = r.add(m)

        p = GenerateJsonFileFromDB()
        p.copy_datasetToModelTraining()

        ooooo = MyClass()
        ooooo.start()
    else:
        if data.status == 'train':
            new_data = data
            new_data.status = 'Идет процесс обучения'
        else:
            new_data = data
            new_data.status = 'Подождите'

    return Response(json.dumps(new_data.to_dict(), ensure_ascii=False), status=200,
                    headers={'Content-Type': 'application/json'})


#
@app.route(API_ROOT + "/ann_json/")
def get_ann_json():
    logger.debug(get_message_by_request(request))
    p = CocoJsonFormatClass()
    p.start_qwe()
    return Response(json.dumps(p.getJsonFull(), ensure_ascii=False, indent=4), status=200,
                    headers={'Content-Type': 'application/json'})


#

@app.route(API_ROOT + '/model_cnn/update/', methods=['POST'])
def update_model():
    logger.debug(get_message_by_request(request))
    data: ModelUnet = ModelUnet(**request.json)
    repo = ModelUnetRepository(1)
    repo.update(data)
    print(data.status)
    return Response('ok', 200)


@app.route(API_ROOT + '/model_cnn/add/', methods=['POST'])
def add_history_model():
    logger.debug(get_message_by_request(request))
    data: ModelUnet = ModelUnet(**request.json)
    repo = ModelUnetRepository(1)
    repo.add(data)
    print(data.status)
    return Response('ok', 200)


@app.route(API_ROOT + '/model_cnn/history/all/', methods=['GET'])
def get_all_history_model_training():
    logger.debug(get_message_by_request(request))
    r = ModelUnetRepository(1)
    data = r.all_history()
    data_list = []
    xml = ReadXmlProject()
    for i in data:
        file_path = os.path.join(str(xml.path_train_model) + str(xml.model_path), str(i.name_file))
        print(file_path)
        if os.path.exists(file_path):
            i = i.to_dict()
            i['download'] = True
            # print(' download true')
        data_list.append(i)
    print(data_list)
    return Response(json.dumps(data_list, ensure_ascii=False), status=200,
                    headers={'Content-Type': 'application/json'})


# if __name__ == '__main__':
    # train_model(request)