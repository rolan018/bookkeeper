from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from typing import Callable, Any


class LabelBox(QtWidgets.QWidget):
    """
    Box with signature
    """

    def __init__(self,
                 label_text: str,
                 checkbox_handler: Callable = None,
                 init_state: Any = Qt.Unchecked,
                 *args,
                 **kwargs):

        super().__init__(*args, **kwargs)

        # layout:
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        # label:
        self.label = QtWidgets.QLabel(label_text)
        self.layout.addWidget(self.label, stretch=1)

        # Checkbox:
        self.check_box = QtWidgets.QCheckBox()
        self.check_box.setCheckState(init_state)
        if checkbox_handler is not None:
            self.check_box.stateChanged.connect(checkbox_handler)
        self.layout.addWidget(self.check_box, stretch=1)


class LabelComboBox(QtWidgets.QWidget):
    """
    Combo Box with signature
    """

    def __init__(self,
                 label_text: str,
                 items: list[str],
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        # layout
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        # Label
        self.label = QtWidgets.QLabel(label_text)
        self.layout.addWidget(self.label, stretch=1)

        # Combo Box with items
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.setEditable(True)
        self.combo_box.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.combo_box.setMaxVisibleItems(16)

        self.items = items
        self.set_items()
        self.layout.addWidget(self.combo_box, stretch=5)

    def clear(self):
        self.combo_box.setCurrentText(self.combo_box.placeholderText())

    def text(self):
        return self.combo_box.currentText()

    def set_items(self):
        self.combo_box.clear()
        self.combo_box.addItems(self.items)

        if len(self.items) != 0:
            self.combo_box.setPlaceholderText(self.items[0])
        else:
            self.combo_box.setPlaceholderText("...")

        self.clear()
