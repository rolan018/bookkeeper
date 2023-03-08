"""
Модуль описывает репозиторий, работающий с базой данных SQLite
"""

import sqlite3
from inspect import get_annotations
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий с базой данных SQLite.
    """
    db_file: str
    table_name: str
    fields: dict[str, Any]
    ob_cls: type

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.ob_cls = cls
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')

    def add(self, obj: T) -> int:
        names_fields = ", ".join(self.fields.keys())
        insert_point = ", ".join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as conn, conn.cursor() as cur:
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names_fields}) VALUES({insert_point})',
                values
            )
            obj.pk = cur.lastrowid
        conn.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        pass

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        pass

    def update(self, obj: T) -> None:
        pass

    def delete(self, pk: int) -> None:
        pass
