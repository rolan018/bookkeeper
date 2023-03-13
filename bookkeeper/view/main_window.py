"""
This is Main Window
"""
from PySide6 import QtWidgets
from bookkeeper.view.table_widgets.label_table import LabelTable
from bookkeeper.view.table_widgets.budget_table import BudgetTable
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category


class MainWindow(QtWidgets.QWidget):
    """
    Application main menu
    """
    def __init__(self,
                 expenses_repo: AbstractRepository[Expense],
                 budget_repo: AbstractRepository[Budget],
                 category_repo: AbstractRepository[Category],
                 *args,
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle('BookKeeper')
        self.layout = QtWidgets.QVBoxLayout()
        #  expanses table
        self.table_1 = LabelTable(expenses_repo, category_repo, 'Последние расходы')
        self.layout.addWidget(self.table_1)
        #  budget table
        self.table_2 = BudgetTable(expenses_repo, budget_repo, category_repo, 'Бюджет')
        self.layout.addWidget(self.table_2)
        self.setLayout(self.layout)
