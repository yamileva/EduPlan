import sqlalchemy
from sqlalchemy import orm
import datetime

from .db_session import SqlAlchemyBase


class Resource(SqlAlchemyBase):
    __tablename__ = 'resources'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    intensity = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    dim = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    section_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("sections.id"))
    duration = sqlalchemy.Column(sqlalchemy.Integer, default=4)
    completed = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    progress = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    activate_date = sqlalchemy.Column(sqlalchemy.DateTime)

    section = orm.relation('Section')
    checks = orm.relation("Check", back_populates='resource')


class Check(SqlAlchemyBase):
    __tablename__ = 'checks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    resource_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("resources.id"))
    completed = sqlalchemy.Column(sqlalchemy.Integer)
    progress = sqlalchemy.Column(sqlalchemy.Integer)
    check_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    check_week = sqlalchemy.Column(sqlalchemy.Integer)

    resource = orm.relation('Resource')

