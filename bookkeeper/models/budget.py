"""
Описан класс, представляющий описание бюджета
"""
from dataclasses import dataclass, field
from datetime import datetime
from bookkeeper.models.expense import Expense


@dataclass(slots=True)
class Budget: # pylint: disable=too-few-public-methods
    """
    Бюджет (совокупность расходов за период времени).
    name - название периода
    begin_period_date - дата начала отсчета
    end_period_date - дата конца отсчета
    value - сумма расходов за данный период
    pk - id записи в базе данных
    """

    name: str = 'Период по умолчанию'
    begin_period_date: datetime = field(default_factory=datetime.now)
    end_period_date: datetime = field(default_factory=datetime.now)
    value: float = 0
    pk: int = 0

    def calculate(self, data: list[Expense]) -> float:
        """
        Function calculates all expanses for given period"""
        tmp = 0.
        for element in data:
            if element.expense_date <= self.end_period_date:
                if element.expense_date >= self.begin_period_date:
                    tmp += float(element.amount)
        return tmp