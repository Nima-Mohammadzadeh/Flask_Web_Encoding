from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class serialNumber(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    CurrentSerial: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)


    def __repr__(self):
        return '<Serial: {}>'.format(self.CurrentSerial)
    