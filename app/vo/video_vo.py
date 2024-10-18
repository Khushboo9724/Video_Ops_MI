from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from app.db.database import Database

database = Database()
engine = database.get_db_connection()
Base = declarative_base()


class VideoVO(Base):
    __tablename__ = "video_table"
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(150), nullable=False)
    path = Column(String(200), nullable=False)
    size = Column(Float, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_on = Column(String(30))
    modified_on = Column(String(30), nullable=False)


    @staticmethod
    def serialize(data):
        return {
            "video_id": data.id,
            "file_name": data.file_name,
            "path": data.path,
            "size": data.size
        }


Base.metadata.create_all(engine)

