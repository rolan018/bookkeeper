"""
Модуль описывает репозиторий, работающий с базой данных SQLite
"""
import sqlite3
from inspect import get_annotations
from typing import Any

from bookkeeper.utils import _type_converter
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
        if getattr(obj, 'pk', False):
            raise ValueError(f'Cannot add object {obj} with existing "pk" attribute')
        values = [getattr(obj, x) for x in self.fields]
        names_field = ", ".join(self.fields.keys())
        insert_point = ", ".join("?" * len(self.fields))
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'CREATE TABLE IF NOT EXISTS {self.table_name} ' +
                _type_converter(self.fields)
            )
            cur.execute(
                f'INSERT INTO {self.table_name} ({names_field}) VALUES({insert_point})',
                values
            )
            obj.pk = cur.lastrowid
        conn.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            try:
                row = cur.execute(
                    f'SELECT * FROM {self.table_name} WHERE ROWID=={pk};'
                ).fetchone()
                if row is None:
                    return None
                kwargs = dict(zip(self.fields, row))
                obj = self.ob_cls(**kwargs)
                obj.pk = pk
                return obj
            except sqlite3.Error as err:
                print(f"[ERROR]:Get method error:{str(err)}")
                return None
        conn.close()

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            try:
                if where is None:
                    rows = cur.execute(
                        f'SELECT ROWID, * FROM {self.table_name} '
                    ).fetchall()
                else:
                    limitations = " AND ".join(f"{f} = ?" for f in where.keys())
                    rows = cur.execute(
                        f'SELECT ROWID, * FROM {self.table_name} '
                        + f'WHERE {limitations}',
                        list(where.values())
                    ).fetchall()
                obj_list = []
                for row in rows:
                    kwargs = dict(zip(self.fields, row[1:]))
                    obj = self.ob_cls(**kwargs)
                    obj.pk = row[0]
                    obj_list.append(obj)
                return obj_list
            except sqlite3.Error as err:
                print(f"[ERROR]:Get_All method error:{str(err)}")
                return []
        conn.close()

    def update(self, obj: T) -> None:
        limitations = ", ".join(f"{field} = ?" for field in self.fields.keys())
        values = [getattr(obj, f) for f in self.fields]
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            try:
                cur.execute(
                    f'UPDATE {self.table_name} SET {limitations} '
                    + f'WHERE ROWID=={obj.pk}',
                    values
                )
                if cur.rowcount == 0:
                    raise ValueError('[ERROR]:Attempt to update' +
                                     ' object with unknown primary key')
            except sqlite3.Error as err:
                print(f"[ERROR]:Update method error:{str(err)}")
        conn.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    f'DELETE FROM {self.table_name} WHERE ROWID=={pk};'
                )
                if cur.rowcount == 0:
                    raise ValueError('[ERROR]:Аttempt to delete object' +
                                     ' with unknown primary key')
            except sqlite3.Error as err:
                print(f"[ERROR]:Delete method error:{str(err)}")
        conn.close()
