# python
import os
import pymysql
from dotenv import load_dotenv


file_path = os.path.abspath(__file__)
directory = os.path.dirname(file_path)
env_file_path = os.path.join(directory, ".env")
load_dotenv(env_file_path)


class MysqlConnector:
    # .env 파일은 github에 업로드하지 않음
    _host = os.getenv("HOST")
    _port = int(os.getenv("SSH_PORT"))
    _user = os.getenv("LOGIN_USER")
    _password = os.getenv("PASSWORD")

    def __init__(self):
        raise TypeError(f'유틸리티 클래스 {self.__name__}에 대한 인스턴스 생성 시도')

    @classmethod
    def connect_db(cls, db_name):
        con = pymysql.connect(host=cls._host, port=cls._port, user=cls._user,
                              password=cls._password, db=db_name, charset="utf8")
        return con
