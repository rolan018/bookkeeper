"""
    Script for starting app
"""

import sys

from PySide6 import QtWidgets

from bookkeeper.view.main_window import MainWindow
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree


if __name__ == '__main__':

    exp_repo_sql = SQLiteRepository[Expense]('bookkeeper.db', Expense)
    cat_repo_sql = SQLiteRepository[Category]('bookkeeper.db', Category)
    bud_repo_sql = SQLiteRepository[Budget]('bookkeeper.db', Budget)

    cats = '''
    продукты
        мясо
            сырое мясо
            мясные продукты
        сладости
    книги
    одежда
    билеты
    '''.splitlines()

    Category.create_from_tree(read_tree(cats), cat_repo_sql)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(exp_repo_sql, bud_repo_sql, cat_repo_sql)
    window.show()
    app.exec()
