"""
Budget Table stands for Manipulate with repository using Budget.
"""
from bookkeeper.view.table_widgets.label_table import LabelTable
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category


class BudgetTable(LabelTable):
    """
    Budget Table
    """
    def __init__(self,
                 expense_repo: AbstractRepository[Expense],
                 budget_repo: AbstractRepository[Budget],
                 category_repo: AbstractRepository[Category],
                 table_name: str,
                 *args,
                 **kwargs) -> None:
        super().__init__(repo=budget_repo,
                         category_repo=category_repo,
                         table_name=table_name,
                         *args,
                         **kwargs)
        # Titles
        self.window_title_delete = 'Удалить бюджет'
        self.window_title_add = 'Добавить бюджет'

        # rep additionally
        self.expense_repo = expense_repo

    def refresh_click(self) -> None:
        """
        Refresh the table
        """
        data = self.expense_repo.get_all()
        for period in self.repo.get_all():
            cur_val = period
            cur_val.value = period.calculate(data)
            self.repo.update(cur_val)
        super().refresh_click()
