import sqlite3
import pytest
from dataclasses import dataclass

from bookkeeper.repository.sqlite_repository import SQLiteRepository


@dataclass
class Custom():
    field_1: int
    field_2: str
    pk: int = 0


@pytest.fixture
def repo():
    return SQLiteRepository(db_file="TEST_DB_REPO.db", cls=Custom)


def test_crud(repo):
    obj1 = Custom(field_1=1, field_2='value_1')
    pk1 = repo.add(obj1)
    obj2 = Custom(field_1=2, field_2='value_2')
    pk2 = repo.add(obj2)
    assert obj1 == repo.get(pk1)  # saves correctly
    assert obj1 != repo.get(pk2)  # different keys
    obj3 = Custom(field_1=3, field_2='value_3')
    obj3.pk = obj1.pk
    repo.update(obj3)
    assert repo.get(pk1) == obj3  # the recording changed
    repo.delete(pk2)
    assert repo.get(pk2) is None


def test_cannot_add_with_pk(repo):
    obj = Custom(field_1=3, field_2='value_3', pk=1)
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_update_unexistent(repo):
    obj = Custom(field_1=3, field_2='value_3', pk=1000)
    with pytest.raises(ValueError):
        repo.update(obj)


def test_cannot_update_without_pk(repo):
    obj = Custom(field_1=4, field_2="value_4")
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_unexistent(repo):
    assert repo.get(-1) is None


def test_cannot_delete_unexistent(repo):
    with pytest.raises(ValueError):
        repo.delete(-1)


def test_get_all(repo):
    objects = [Custom(field_1=i, field_2=f'value_{i}') for i in range(10, 15)]
    for obj in objects:
        repo.add(obj)
    for idx, ob in enumerate(repo.get_all()):
        assert ob.pk == objects[idx].pk


def test_get_all_with_condition(repo):
    objects = []
    for i in range(5):
        o = Custom(field_1=1, field_2='value_1')
        o.field_1 = i
        o.field_2 = 'test'
        repo.add(o)
        objects.append(o)
    object_get_pk = [o.pk for o in repo.get_all({'field_1': 0})]
    assert object_get_pk[0] == objects[0].pk
    objects_get_pk = [o.pk for o in repo.get_all({'field_2': 'test'})]
    assert objects_get_pk == [o.pk for o in objects]