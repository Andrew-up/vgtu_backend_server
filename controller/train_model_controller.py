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
    """
    Этот обработчик маршрута принимает HTTP GET запрос на `/model_cnn/last_model/` и возвращает последнюю историю тренировки модели. Он использует `ModelUnetRepository` для получения последней истории тренировки и преобразует данные в формат JSON. Если данные существуют, возвращается объект `Response` с кодом статуса 200 и содержимым в формате JSON. Если данных нет, возвращается объект `Response` с пустыми данными.

    :returns: Последняя история тренировки модели в формате JSON или пустой объект JSON
    :rtype: Response

    Примеры:

    .. code-block:: python

        Входные данные: GET /model_cnn/last_model/
        Ожидаемый результат: Последняя история тренировки модели в формате JSON

    """
    logger.debug(get_message_by_request(request))
    r = ModelUnetRepository(1)
    void_history = ModelUnet()
    data = r.get_last_history_train()
    if data.id:
        data = data.to_dict()
        return Response(json.dumps(data, ensure_ascii=False), status=200,
                        headers={'Content-Type': 'application/json'})
    return Response(json.dumps(void_history.to_dict(), ensure_ascii=False), status=200,
                    headers={'Content-Type': 'application/json'})


@app.route(API_ROOT + '/model_cnn/last_model/download/')
def get_last_history_download():
    """

    Этот обработчик маршрута принимает HTTP GET запрос на `/model_cnn/last_model/download/` и возвращает файл для скачивания. Он принимает параметр `version` из запроса. Если параметр не указан, возвращается сообщение "Укажите версию для загрузки".

    :returns: Файл для скачивания или сообщение об ошибке
    :rtype: Response или str

    Примеры:

    .. code-block::

        Входные данные: GET /model_cnn/last_model/download/?version=2.0
        Ожидаемый результат: Файл с именем "2.0.zip" для скачивания

        Входные данные: GET /model_cnn/last_model/download/
        Ожидаемый результат: Сообщение "Укажите версию для загрузки"

    """
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
    """
    Эта функция принимает строку версии и генерирует новую версию на ее основе. Если версия не указана, по умолчанию используется '1.0.0'. Функция возвращает новую версию в виде строки.

    :param version: (Опционально) Входная строка версии (по умолчанию None)
    :type version: str

    :returns: Новая версия в виде строки
    :rtype: str

    Примеры:

    .. code-block:: python

        Входные данные: generate_new_version('1.2.3')
        Ожидаемый результат: '1.2.4'

        Входные данные: generate_new_version('2.1.99')
        Ожидаемый результат: '2.2.0'

        Входные данные: generate_new_version('3.99.99')
        Ожидаемый результат: '4.0.0'

        Входные данные: generate_new_version()
        Ожидаемый результат: '1.0.0'

    """
    version_str = '1.0.0'
    # print(version)
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
    """

    Этот обработчик маршрута принимает HTTP POST или GET запросы на `/model_cnn/delete/<id>`. Если метод запроса - POST, функция проверяет наличие ключа `key` в теле запроса, и если ключ совпадает с `SECRET_KEY`, происходит удаление модели с указанным `id` из репозитория. Если метод запроса - GET, функция возвращает ошибку доступа.

    :param id: Идентификатор модели
    :type id: str

    :returns: Статус операции удаления или сообщение об ошибке доступа
    :rtype: Response или str

    Примеры:

    .. code-block:: python

        Входные данные (POST): /model_cnn/delete/1, {"key": "my-secret-key"}
        Ожидаемый результат: Статус операции удаления модели с идентификатором 1

        Входные данные (POST): /model_cnn/delete/2, {"key": "wrong-key"}
        Ожидаемый результат: Ошибка доступа

        Входные данные (GET): /model_cnn/delete/1
        Ожидаемый результат: Ошибка доступа
    """
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

    """
    Добавляет запись в бд с новой ModelUnet
    и запускает класс MyClass в отдельном потоке

    .. warning::
        - Сейчас это сделано с помощью запуска субпроцесса.
        - Требуется в проекте для тренировки модели сделать API.
        - Если сейчас приложение запускать в контейнере, работать не будет.

    :return: JSON
    """

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
    """
    Возвращает список всех изображений которые используются для обучения CNN и список аннотаций к ним в формате COCO.

    Прочитать про COCO формат можно `тут <https://cocodataset.org/#format-data>`_

    :return: JSON содержащий файл аннотации COCO
    """
    logger.debug(get_message_by_request(request))
    p = CocoJsonFormatClass()
    p.start_qwe()
    return Response(json.dumps(p.getJsonFull(), ensure_ascii=False, indent=4), status=200,
                    headers={'Content-Type': 'application/json'})


#

@app.route(API_ROOT + '/model_cnn/update/', methods=['POST'])
def update_model():

    """
    Код представляет собой обработчик POST запроса на URL /api/model_cnn/update/. Входные данные передаются в формате JSON и проверяются на соответствие модели ModelUnet. Затем данные обновляются в репозитории ModelUnetRepository. Код также выводит статус данных (data.status) и возвращает ответ 'ok' с кодом 200.

    Примеры входных и выходных данных.

    Входные данные:

    .. code-block:: json

        {
            "name_file": "model_1_0_4.tflite",
            "path_dataset": "1_0_4",
            "id": 5,
            "time_train": "время обучения: 00 часов 02 минут 24 секунд",
            "total_epochs": 2,
            "accuracy": null,
            "output_size": "[256 256 10]",
            "current_epochs": 2,
            "quality_dataset": 2,
            "status": "completed",
            "quality_train_dataset": 1,
            "input_size": "[256, 256, 3]",
            "date_train": "15-August-2023 16:28:04",
            "quality_valid_dataset": 1,
            "num_classes": 9,
            "version": "1.0.4"
        }

    Выходные данные:

        ОК (ответ сервера)

    """
    logger.debug(get_message_by_request(request))
    data: ModelUnet = ModelUnet(**request.json)
    repo = ModelUnetRepository(1)
    repo.update(data)
    print(data.status)
    return Response('ok', 200)


@app.route(API_ROOT + '/model_cnn/add/', methods=['POST'])
def add_history_model():


    """
    Код представляет собой обработчик POST запроса на URL /api/model_cnn/add/.
    Входные данные передаются в формате JSON и проверяются на соответствие модели ModelUnet.
    Затем данные обновляются в репозитории ModelUnetRepository. Код также выводит статус данных (data.status) и возвращает ответ 'ok' с кодом 200.

    Примеры входных и выходных данных.

    Входные данные:

    .. code-block:: json

        {
            "id": 5,
            "total_epochs": 2,
            "version": "1.0.4"
        }


    Выходные данные:

        OK (ответ сервера)

    """
    logger.debug(get_message_by_request(request))
    data: ModelUnet = ModelUnet(**request.json)
    repo = ModelUnetRepository(1)
    repo.add(data)
    print(data.status)
    return Response('ok', 200)


@app.route(API_ROOT + '/model_cnn/<id>/', methods=['GET'])
def check_model_by_id(id):
    """
    Обработчик GET-запроса на URL `/api/model_cnn/<id>/`.

    :param id: идентификатор модели
    :type id: int
    :return: JSON-ответ с информацией о модели
    :rtype: Response

    Примеры входных и выходных данных:

    - Входные данные: `id` - идентификатор модели (например, 3)
      Выходные данные (JSON-ответ в случае успеха):

      .. code-block:: json

        {
            "id_model": 3,
            "name": "Модель 1",
            "download": true
        }

      В случае отсутствия файла модели:

      .. code-block:: json

        {
            "id_model": 3,
            "name": "Модель 1"
        }

    """
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
    """
    Возвращает список всех историй доступных для загрузки.

    Тоже самое что и get_last_history_download() только вовзращает список историй.

    :return: Список историй доступтных для загрузки.
    """
    logger.debug(get_message_by_request(request))
    r = ModelUnetRepository(1)
    data = r.all_history()
    data_list = []
    xml = ReadXmlProject()
    for i in data:
        file_path = os.path.join(str(xml.path_train_model) + str(xml.model_path), str(i.name_file))
        i = i.to_dict()
        if os.path.exists(file_path):
            i['download'] = True
        data_list.append(i)
    return Response(json.dumps(data_list, ensure_ascii=False, indent=4), status=200,
                    headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    p = CocoJsonFormatClass()
    p.start_qwe()
    train_model()
