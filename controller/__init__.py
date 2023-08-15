from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

# корневой для для приложения пример: localhost:8080/API_ROOT -> localhost:8080/api
API_ROOT = '/api/'

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


class Client:
    ip_client = None,
    url = None


# получает IP и url и возвращает строку, используется для логгирования
def get_message_by_request(req: request):
    client = Client()
    client.ip_client = req.remote_addr
    client.url = req.path
    message = f'IP CLIENT:{client.ip_client}, URL_API: {client.url}'
    return message


def read_file_chunks(path):
    CHUNK_SIZE = 8192
    with open(path, 'rb') as fd:
        while 1:
            buf = fd.read(CHUNK_SIZE)
            if buf:
                yield buf
            else:
                break



def create_app():
    """
    Инициализация всех маршрутов приложения
    app_controller - маршруты приложения, нет связи с бд
    patient_controller - маршруты для взаимодействия с таблицей пациентов
    healing_history_controller - маршруты для взаимодействия с таблицей история лечения пациентов
    result_predict_controller - маршруты для взаимодействия  с таблицей результатов распознавания
    train_model_controller - маршруты для запуска субпроцессов обучения модели, загрузка модели
    """
    import controller.app_controller
    import controller.patient_controller
    import controller.healing_history_controller
    import controller.result_predict_controller
    import controller.train_model_controller
    return app
