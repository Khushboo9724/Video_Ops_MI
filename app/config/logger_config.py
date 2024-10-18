import contextvars
import logging
import os

from app.custom_enum.server_enum import ServerEnvEnum

request_id_context_var = contextvars.ContextVar("request_id", default=None)

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

LOG_FILE_PATH = os.path.join(basedir, "logs")

LOG_LEVEL = logging.DEBUG

LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(request_id)s %(filename)s:%(lineno)s - %(funcName)2s() : %(message)s\n'

env = ServerEnvEnum.LOCAL_ENV


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:

        record.request_id = request_id_context_var.get()
        return True


class MaxByteLengthFormatter(logging.Formatter):

    def __init__(self, fmt=None, datefmt=None, max_byte_length=250000):
        super().__init__(fmt, datefmt)  # Use Python 3 style super()
        self.max_byte_length = max_byte_length

    def format(self, record):

        original_msg = super().format(record)  # Use Python 3 style super()
        original_byte_length = len(original_msg.encode('utf-8'))

        if original_byte_length <= self.max_byte_length:
            return original_msg

        truncated_msg = original_msg.encode('utf-8')[:self.max_byte_length] + (
            b'...' if original_byte_length > self.max_byte_length else b'')
        return truncated_msg.decode('utf-8')


class MyLogger:

    @staticmethod
    def get_logger(logger_name=None):
        logging.basicConfig()
        logger = logging.getLogger(logger_name)
        logger.setLevel(LOG_LEVEL)

        log_file = None  # Assign a default value

        if not env:
            if env.lower() == "dev":
                log_file = os.path.join(LOG_FILE_PATH, "dev.log")
            elif env.lower() == "prod":
                log_file = os.path.join(LOG_FILE_PATH, "prod.log")
            elif env.lower() == "uat":
                log_file = os.path.join(LOG_FILE_PATH, "uat.log")

        if log_file:
            file_handler = logging.FileHandler(log_file)
        else:
            file_handler = logging.StreamHandler()

        byte_formatter = MaxByteLengthFormatter(LOG_FORMATTER)
        file_handler.setFormatter(byte_formatter)
        file_handler.addFilter(RequestIdFilter())
        logger.addHandler(file_handler)

        return logger
