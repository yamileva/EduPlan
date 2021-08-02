import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Track(SqlAlchemyBase):
    __tablename__ = 'tracks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False,
                              index=True)
    last_visit = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    is_public = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    progress = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    user = orm.relation('User')
    sections = orm.relation("Section", back_populates='track')

    def on_delete(self, session):
        for section in self.sections:
            section.on_delete(session)
            session.delete(section)

