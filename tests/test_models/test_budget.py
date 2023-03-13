from datetime import datetime, timedelta

import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_with_full_args_list():
    e = Budget(name="Тест бюджет", begin_period_date=datetime.now(),
               end_period_date=datetime.now(), value=250, pk=1)

    assert e.name == "Тест бюджет"
    assert e.value == 250


def test_create_brief():
    e = Budget()
    assert e.name == 'Период по умолчанию'
    assert e.value == 0


def test_can_add_to_repo(repo):
    e = Budget(name="Тест Бюджет")
    pk = repo.add(e)
    assert e.pk == pk


def test_calculate(repo):
    b = Budget(name="Тест Бюджет",
               begin_period_date=datetime.now()-timedelta(1),
               end_period_date=datetime.now()+timedelta(1))
    e_1 = Expense(100, 1)
    e_2 = Expense(200, 1)
    b.calculate([e_1, e_2])

    assert b.calculate([e_1, e_2]) == 300
