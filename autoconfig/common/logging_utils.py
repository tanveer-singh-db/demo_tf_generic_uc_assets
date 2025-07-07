import logging
from io import StringIO
import sys

APP_LOGGER_NAME = 'autoconfig'

d_log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'fatal': logging.FATAL
}

def get_app_level_logger(
    logger_name: str = APP_LOGGER_NAME,
     log_level: str = 'debug',
     log_buffer: StringIO = None,
     log_file: str = None):
    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():
        return logger
    log_level = d_log_levels.get(log_level.strip().lower(), logging.DEBUG)
    # print(log_level)
    logger.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt='%y-%m-%d %H:%M:%S')
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(sh)

    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if log_buffer:
        fh = logging.StreamHandler(log_buffer)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def get_log(module_name: str = None, log_level: str = 'debug', app_logger_name: str = APP_LOGGER_NAME, log_file=None):
    app_level_logger = get_app_level_logger(logger_name=app_logger_name, log_level=log_level, log_file=log_file)
    return app_level_logger.getChild(module_name) if module_name else app_level_logger

