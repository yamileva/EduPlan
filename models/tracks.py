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

    def sections_to_table(self):
        if not self.sections:
            return [[]]
        bottom_sect = max(self.sections, key=lambda sect: sect.row + sect.rows - 1)
        rows = bottom_sect.row + bottom_sect.rows - 1
        table_sections = [list() for _ in range(rows)]
        sorted_sections = sorted(self.sections, key=lambda section: -section.rows)
        for item in sorted_sections:
            table_sections[item.row - 1].append(item)
            if item.rows > 1:
                for i in range(item.rows - 1):
                    table_sections[item.row + i].append(0)
        return table_sections
