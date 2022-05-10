import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Lesson(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    typing_text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    done = sqlalchemy.Column(sqlalchemy.Boolean)
    average_speed = sqlalchemy.Column(sqlalchemy.Float)
    time = sqlalchemy.Column(sqlalchemy.String)
