import logging
import os
from datetime import datetime

from definitions import LOG_DIR


LOGGER_FORMAT = '[%(asctime)s]\t[%(filename)s > %(funcName)s]\t[%(levelname)s] > %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'

print('Данный проект использует логгирование')
print(f'Логи хранятся в директории: [{LOG_DIR}]')


# def get_level_logging(level: str) -> str:
#     match level.upper():
#         case 'CRITICAL' | 'C' | 'CRIT':
#             return 'CRITICAL'
#         case 'ERROR' | 'E' | 'ERR':
#             return 'ERROR'
#         case 'WARNING' | 'W' | 'WARN':
#             return 'WARNING'
#         case 'INFO' | 'I' | 'INF':
#             return 'INFO'
#         case 'DEBUG' | 'D' | 'DEB':
#             return 'DEBUG'


def get_custom_logger(filename=None, dir_file=None, subdirectory=None, name_logging='api') -> logging:
    # name_logging = get_level_logging(name_logging).lower()

    logger_name = f'{name_logging}_logging_file'
    if logger_name in logging.root.manager.loggerDict:
        return logging.getLogger(logger_name)

    custom_logging = logging.getLogger(logger_name)
    custom_logging.propagate = False
    if filename is None:
        filename = '{}_{}.log'.format(datetime.today().strftime('%d-%m-%Y'), logger_name)
    if dir_file is None:
        dir_file = LOG_DIR
    if subdirectory is None:
        subdirectory = datetime.today().strftime('%d-%m-%Y')
    final_path_logfile = os.path.join(dir_file, subdirectory, filename)
    if not os.path.exists(os.path.join(dir_file, subdirectory, filename)):
        os.makedirs(os.path.join(dir_file, subdirectory), exist_ok=True)
    file = logging.FileHandler(final_path_logfile)
    file.setFormatter(logging.Formatter(LOGGER_FORMAT, datefmt=datefmt))
    custom_logging.addHandler(file)
    # match name_logging.upper():
    #     case 'CRITICAL':
    #         custom_logging.setLevel(level=logging.CRITICAL)
    #     case 'ERROR':
    #         custom_logging.setLevel(level=logging.ERROR)
    #     case 'WARNING':
    #         custom_logging.setLevel(level=logging.WARNING)
    #     case 'INFO':
    #         custom_logging.setLevel(level=logging.INFO)
    #     case 'DEBUG':
    #         custom_logging.setLevel(level=logging.DEBUG)
    return custom_logging


if __name__ == '__main__':
    pass
