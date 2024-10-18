from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.service.common.common_service import AppServices
from app.utils import constant

DB_HOST = constant.DB_HOST
DB_USERNAME = constant.DB_USERNAME
DB_PASSWORD = constant.DB_PASSWORD
DB_PORT = constant.DB_PORT
DB_NAME = constant.DB_NAME

MYSQL_URL = \
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"
POOL_SIZE = 10
POOL_RECYCLE = 3600
POOL_TIMEOUT = 15
MAX_OVERFLOW = 0
CONNECT_TIMEOUT = 60
PREPING = True


class Database:

    _instance = None

    def __init__(self):
        self.engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection_is_active = False
            cls._instance.engine = None
        return cls._instance

    def get_db_connection(self):

        if not self.connection_is_active:
            connect_args = {"connect_timeout": CONNECT_TIMEOUT}
            try:
                self.engine = create_engine(
                    MYSQL_URL,
                    pool_size=POOL_SIZE,
                    pool_recycle=POOL_RECYCLE,
                    pool_timeout=POOL_TIMEOUT,
                    max_overflow=MAX_OVERFLOW,
                    connect_args=connect_args,
                    pool_pre_ping=PREPING
                )
                return self.engine
            except Exception as exception:
                AppServices.handle_exception(exception, is_raise=True)
        return self.engine

    @staticmethod
    def get_db_session(engine):

        try:
            db_session = sessionmaker(bind=engine)
            session = db_session()
            return session
        except Exception as exception:
            AppServices.handle_exception(exception, is_raise=True)
