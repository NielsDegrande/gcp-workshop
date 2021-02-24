# -*- coding: utf-8 -*-

import os
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.dao.base import initialize_db

_engine = create_engine(os.getenv("CONNECTION_STRING"))
initialize_db(_engine)


class Session:
    def __init__(self):
        self._engine = _engine

    def __enter__(self):
        self._session = sessionmaker(bind=self._engine)()
        return self

    def __exit__(self, *_):
        self._session.commit()
        self._session.close()

    def add(self, item: Any) -> None:
        self._session.add(item)
