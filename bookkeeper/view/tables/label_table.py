"""
Label Table stands for Manipulate with repository.
"""

from PySide6 import QtWidgets
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from bookkeeper.view.simple_widgets.boxes import LabelComboBox
from bookkeeper.view.simple_widgets.lines import LabelLine
from bookkeeper.view.simple_widgets.date_time import DateTimeWidget
from bookkeeper.models.category import Category


class LabelTable(QtWidgets.QWidget):
    """
    Label TABLE
    """
    def __init__(self,
                 repo: AbstractRepository[T],
                 category_repo: AbstractRepository[Category],
                 table_name: str,
                 *args,
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Titles
        self.window_title_delete = 'Удалить покупку'
        self.window_title_add = 'Добавить покупку'

        # list categories
        self.repo = repo
        self.category_repo = category_repo
        self.layout = QtWidgets.QGridLayout()

        self.table_name = QtWidgets.QLabel(table_name)
        self.layout.addWidget(self.table_name, 0, 0, 1, 1)
        self.btn = QtWidgets.QPushButton('Обновить')
        self.btn.clicked.connect(self.refresh_click)
        self.layout.addWidget(self.btn, 0, 1, 1, 1)

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_menu)
        self.layout.addWidget(self.add_btn, 0, 2, 1, 1)

        self.delete_btn = QtWidgets.QPushButton('Удалить')
        self.delete_btn.clicked.connect(self.del_menu)
        self.layout.addWidget(self.delete_btn, 0, 3, 1, 1)

        self.exp_tabl = QtWidgets.QTableWidget(20, len(self.repo.fields) + 1)
        for i, element in enumerate(self.repo.fields.keys()):
            self.exp_tabl.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(element))
        self.exp_tabl.setHorizontalHeaderItem(len(self.repo.fields),
                                              QtWidgets.QTableWidgetItem('PK'))
        self.layout.addWidget(self.exp_tabl, 1, 0, 1, 40)
        self.setLayout(self.layout)
        self.dlg = QtWidgets.QDialog()
        self.dlg_widgets = []

    def refresh_click(self) -> None:
        """
        pass
        """
        result = self.repo.get_all()
        to_table = []
        for element in result:
            values = [getattr(element, x) for x in self.repo.fields]
            values.append(getattr(element, 'pk'))
            to_table.append(values)
        self.exp_tabl.clearContents()
        self.add_data(to_table)

    def add_menu(self) -> None:
        """
        pass
        """
        self.dlg = QtWidgets.QDialog()
        self.dlg.setWindowTitle(self.window_title_add)
        layout = QtWidgets.QVBoxLayout()
        self.dlg_widgets = []
        for element in self.repo.fields.items():
            if element[0] == 'category':
                # get categories from category repo
                cats = [cat.name for cat in self.category_repo.get_all()]
                label_combo_box = LabelComboBox(label_text=element[0],
                                                items=cats)
                layout.addWidget(label_combo_box)
                self.dlg_widgets.append(label_combo_box)
            elif 'date' in element[0]:
                date_time_box = DateTimeWidget(label_text=str(element[0]))
                layout.addWidget(date_time_box)
                self.dlg_widgets.append(date_time_box)
            else:
                if 'int' in str(element[1]) or 'float' in str(element[1]):
                    label_line = LabelLine(label_text=str(element[0]),
                                           place_holder="Введите значение",
                                           validator_type='number')
                else:
                    label_line = LabelLine(label_text=str(element[0]),
                                           place_holder="Введите значение")
                layout.addWidget(label_line)
                self.dlg_widgets.append(label_line)

        add = QtWidgets.QPushButton('Добавить')
        add.clicked.connect(self.add_click)
        layout.addWidget(add)

        cancel = QtWidgets.QPushButton('Отменить')
        cancel.clicked.connect(self.cancel)
        layout.addWidget(cancel)

        self.dlg.setLayout(layout)
        self.dlg.exec()

    def cancel(self) -> None:
        """
        pass
        """
        self.dlg.close()

    def add_click(self) -> None:
        """
        pass
        """
        to_table = [widget.text() for widget in self.dlg_widgets]
        self.repo.add(self.repo.ob_cls(*to_table))
        self.refresh_click()
        self.cancel()

    def del_menu(self) -> None:
        """
        pass
        """
        self.dlg = QtWidgets.QDialog()
        self.dlg.setWindowTitle(self.window_title_delete)
        layout = QtWidgets.QVBoxLayout()
        label_line = LabelLine(label_text="PK",
                               place_holder="Введите PK записи")
        self.dlg_widgets.append(label_line)
        layout.addWidget(label_line)

        add = QtWidgets.QPushButton('Применить')
        add.clicked.connect(self.del_click)
        layout.addWidget(add)

        cancel = QtWidgets.QPushButton('Отменить')
        cancel.clicked.connect(self.cancel)
        layout.addWidget(cancel)
        self.dlg.setLayout(layout)
        self.dlg.exec()

    def del_click(self) -> None:
        """
        pass
        """
        try:
            self.repo.delete(int(self.dlg_widgets[-1].text()))
        except Exception as err:
            print(f'[ERROR]: {str(err)}')
        finally:
            self.refresh_click()
            self.cancel()

    def add_data(self, data: list) -> None:
        """
        pass
        """
        for num_i, row in enumerate(data):
            for num_j, x in enumerate(row):
                self.exp_tabl.setItem(num_i, num_j,
                                      QtWidgets.QTableWidgetItem(str(x)))
