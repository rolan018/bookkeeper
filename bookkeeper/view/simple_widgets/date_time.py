"""
    Widget for processing DATETIME
"""

from PySide6 import QtWidgets
from PySide6.QtCore import QDateTime
from datetime import datetime


class DateTimeWidget(QtWidgets.QWidget):
    """
    Datetime widget
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

    def text(self) -> datetime:
        """
        Return the entered text in the field
        """
        return self.date_time.dateTime().toPython()
