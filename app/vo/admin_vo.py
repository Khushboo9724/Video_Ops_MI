from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

from app.db.database import Database
database = Database()
engine = database.get_db_connection()
Base = declarative_base()


class AdminVO(Base):
    __tablename__ = "user_table"
    __table_args__ = {'mysql_engine': 'InnoDB'}

    user_id = Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False)
    password = Column(String(150), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_on = Column(String(30))
    modified_on = Column(String(30), nullable=False)

    @staticmethod
    def serialize(data):
        return {
            "user_id": data.user_id,
            "first_name": data.firstname,
            "last_name": data.lastname,
            "email": data.email,
            "role": data.role,
        }


# Base.metadata.create_all(engine)
