"""
    pass
"""
from PySide6 import QtWidgets, QtGui


class LabelLine(QtWidgets.QWidget):
    """
    Input field
    Parametrs:
    label_text: str
    place_holder: str
    validator_type: must be string or number
    """

    def __init__(self,
                 label_text: str,
                 place_holder: str,
                 validator_type: str = 'string',
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        # layout
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        # label text
        self.label = QtWidgets.QLabel(label_text)
        self.layout.addWidget(self.label, stretch=1)

        # placeholder text
        self.place_holder = place_holder
        self.name = QtWidgets.QLineEdit()
        self.name.setPlaceholderText(self.place_holder)

        # validators
        if validator_type in 'number string'.split():
            self.validator_type = validator_type
        else:
            raise ValueError(f"Param: validator_type must be 'string' or 'number'")

        if self.validator_type == 'number':
            self.name.setValidator(QtGui.QIntValidator(1, 10_000_000, self))
        elif self.validator_type == 'string':
            self.name.setValidator(QtGui.QRegularExpressionValidator('^[а-яА-ЯёЁa-zA-Z0-9]+$',
                                                                     self))
        self.layout.addWidget(self.name, stretch=5)

    def clear(self):
        self.name.setText(self.place_holder)

    def text(self):
        return self.name.text()