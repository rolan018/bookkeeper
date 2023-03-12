"""
    pass
"""

from PySide6 import QtWidgets
from PySide6.QtCore import QDateTime


class DateTimeWidget(QtWidgets.QWidget):
    """
    Combo Box with signature
    """

    def __init__(self,
                 label_text: str,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        # layout
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        # label
        self.label = QtWidgets.QLabel(label_text)
        self.layout.addWidget(self.label, stretch=1)

        # datetime
        self.date_time = QtWidgets.QDateTimeEdit()
        self.date_time.setDateTime(QDateTime.currentDateTime())
        self.layout.addWidget(self.date_time, stretch=1)

    def text(self):
        """
        pass
        """
        return self.date_time.dateTime().toPython()
