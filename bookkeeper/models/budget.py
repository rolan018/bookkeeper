"""
Модель бюджета
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Budget:
    """
    Бюджет
    begin_period_date - начало
    end_period_date - конец
    value - сумма расходов
    pk - id в бд
    """

    begin_period: datetime = field(default_factory=datetime.now)
    end_period: datetime = field(default_factory=datetime.now)
    value: float = 0
    limit: float = 0
    pk: int = 0