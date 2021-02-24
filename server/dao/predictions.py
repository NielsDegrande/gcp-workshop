# -*- coding: utf-8 -*-

from sqlalchemy import Column, DateTime, Integer, String

from server.dao.base import Base


class Predictions(Base):
    __tablename__ = "predictions"

    id = Column("id", Integer, primary_key=True)
    request_time = Column("request_time", DateTime)
    request = Column("request", String)
    quantity = Column("quantity", Integer, nullable=True)
