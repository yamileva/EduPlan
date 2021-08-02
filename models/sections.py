import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Section(SqlAlchemyBase):
    __tablename__ = 'sections'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    track_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("tracks.id"))
    type = sqlalchemy.Column(sqlalchemy.Integer, default=0) # не нужен?  или учесть подвал?
    row = sqlalchemy.Column(sqlalchemy.Integer, default=1)

    duration = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    progress = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    track = orm.relation('Track')
    resources = orm.relation("Resource", back_populates='section')

    def on_delete(self, session, alldel=False):
        for resource in self.resources:
            resource.on_delete(session)
            session.delete(resource)
        if alldel:
            return
        track = self.track
        for item in track.sections:
            if item.row > self.row:
                item.row -= 1
