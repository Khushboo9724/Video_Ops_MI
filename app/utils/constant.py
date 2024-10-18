from configparser import ConfigParser
import os
configure = ConfigParser()


ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

configure.read(
    f"{ROOT_DIR}/config.ini"
)

DB_HOST = configure.get('DB_CONFIG', 'db_host')
DB_USERNAME = configure.get('DB_CONFIG', 'db_username')
DB_PASSWORD = configure.get('DB_CONFIG', 'db_password')
DB_PORT = configure.get('DB_CONFIG', 'db_port')
DB_NAME = configure.get('DB_CONFIG', 'db_name')

REDIS_HOST = configure.get('REDIS_CONFIG', 'redis_host')
REDIS_PORT = configure.get('REDIS_CONFIG', 'redis_port')

secrets_key = configure.get("Secret_Key", "secret_key")
