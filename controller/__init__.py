from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

API_ROOT = '/api/'

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

CHUNK_SIZE = 8192


class Client:
    ip_client = None,
    url = None


def get_message_by_request(req: request):
    client = Client()
    client.ip_client = req.remote_addr
    client.url = req.path
    message = f'IP CLIENT:{client.ip_client}, URL_API: {client.url}'
    return message


def read_file_chunks(path):
    with open(path, 'rb') as fd:
        while 1:
            buf = fd.read(CHUNK_SIZE)
            if buf:
                yield buf
            else:
                break


def create_app():
    import controller.app_controller
    import controller.patient_controller
    import controller.healing_history_controller
    import controller.result_predict_controller
    import controller.train_model_controller
    return app
