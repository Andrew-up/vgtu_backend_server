import json
import os
import os.path
import subprocess
import threading

from flask import Response, request, stream_with_context

from controller import app, API_ROOT, read_file_chunks, get_message_by_request
from definitions import SECRET_KEY
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


class MyClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.xml = ReadXmlProject()

    def run(self):
        """
        Запускает subprocess в отдельном потоке
        """
        path_script = os.path.join(self.xml.path_train_model, self.xml.name_script)
        subprocess.run(['python3', path_script],
                       executable=self.xml.path_python_interceptor, shell=False)


@app.route(API_ROOT + '/model_cnn/delete/<id>', methods=['POST', 'GET'])
def delete_model_cnn(id):
    if request.method == 'POST':
        r = request.json
        if r['key'] == SECRET_KEY:
            print('delete')
            repo = ModelUnetRepository(1)
            status = repo.delete_by_id(id)
            logger.debug(get_message_by_request(request))
            return Response(json.dumps(status, ensure_ascii=False, indent=4), status=200,
                            headers={'Content-Type': 'application/json'})
    else:
        logger.warning(get_message_by_request(request))
        return Response('Ошибка доступа', 401)


@app.route(API_ROOT + '/model_cnn/train/')
def train_model():
    try:
        logger.debug(get_message_by_request(request))
    except RuntimeError as e:
        print(e)
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


@app.route(API_ROOT + '/model_cnn/<id>/', methods=['GET'])
def check_model_by_id(id):
    r = ModelUnetRepository(1)
    res = r.get(id_model=id)
    xml = ReadXmlProject()
    file_path = os.path.join(str(xml.path_train_model) + str(xml.model_path), str(res.name_file))
    if os.path.exists(file_path):
        res = res.to_dict()
        res['download'] = True
    else:
        res = res.to_dict()
    return Response(json.dumps(res, ensure_ascii=False, indent=4), status=200,
                    headers={'Content-Type': 'application/json'})


@app.route(API_ROOT + '/model_cnn/history/all/', methods=['GET'])
def get_all_history_model_training():
    logger.debug(get_message_by_request(request))
    r = ModelUnetRepository(1)
    data = r.all_history()
    print(data)
    data_list = []
    xml = ReadXmlProject()
    for i in data:
        file_path = os.path.join(str(xml.path_train_model) + str(xml.model_path), str(i.name_file))
        print(file_path)
        i = i.to_dict()
        if os.path.exists(file_path):
            i['download'] = True
            # print(' download true')

        data_list.append(i)
    print(data_list)
    return Response(json.dumps(data_list, ensure_ascii=False, indent=4), status=200,
                    headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    p = CocoJsonFormatClass()
    p.start_qwe()
    train_model()
