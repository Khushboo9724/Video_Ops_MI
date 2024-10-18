from app.client.mysql.mysql_query_dao import *
from app.vo.user_vo import UserVO


class UserDAO:
    @staticmethod
    def insert_user_dao(user_vo_create):
        get_data = insert(user_vo_create)
        return get_data

    @staticmethod
    def get_user_by_email_dao(user_email):
        get_data = get_by_email(UserVO, user_email)
        return get_data
