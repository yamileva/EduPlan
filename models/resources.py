import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Resource(SqlAlchemyBase):
    __tablename__ = 'resources'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    section_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("sections.id"))
    duration = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    progress = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    section = orm.relation('Section')