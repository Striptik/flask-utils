import logging
import os
from logging import StreamHandler

from requests_futures.sessions import FuturesSession


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatadogHttpHandler:
    def __init__(
        self, api_key, service, host, source, logger_name="", level=None, raise_exception=False
    ):

        self.api_key = api_key
        self.service = service
        self.host = host
        self.source = source
        self.raise_exception = raise_exception
        self.setup_logger(logger_name, level)

    def setup_logger(self, logger_name, level):
        if level is None:
            level = logging.INFO

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)
        self.logger.addHandler(self.setup_handler(level))

    def setup_handler(self, level):
        handler = DataDogHandler(
            self.api_key, service=self.service, host=self.host, source=self.source, raise_exception=self.raise_exception
        )
        handler.setLevel(level)
        return handler


class DataDogHandler(StreamHandler):
    def __init__(self, api_key, service, host, source, raise_exception=False):
        StreamHandler.__init__(self)
        self.source = source
        self.service = service
        self.host = host
        self.env = os.getenv("ENVIRONMENT", "dev")
        self.raise_exception = raise_exception
        self.headers = {"Content-Type": "application/json"}
        self.url = "https://browser-http-intake.logs.datadoghq.eu/v1/input/" + api_key

    def emit(self, record):
        payload = {
            "message": record.msg,
            "level": record.levelname,
            "metas": record.args,
        }
        if self.service:
            payload["service"] = self.service
            payload["hostname"] = self.host
            payload["ddsource"] = self.source
            payload["env"] = self.env


        session = FuturesSession()
        try:
            session.post(self.url, json=payload, headers=self.headers)
        except Exception:
            return


class DatadogSingletonHttpHandler(DatadogHttpHandler, metaclass=Singleton):
    pass
