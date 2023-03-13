"""
    Widget for processing combo values
"""
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


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

        # label for description
        self.label = QtWidgets.QLabel(label_text)
        self.layout.addWidget(self.label, stretch=1)

        # Combo box widget
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.setEditable(True)
        self.combo_box.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.combo_box.setMaxVisibleItems(16)

        self.items = items
        self.set_items()
        self.layout.addWidget(self.combo_box, stretch=5)

    def clear(self) -> None:
        """
        Сlear the field
        """
        self.combo_box.setCurrentText(self.combo_box.placeholderText())

    def text(self) -> str:
        """
        Return the entered text in the field
        """
        return self.combo_box.currentText()

    def set_items(self) -> None:
        """
        Set values to fields
        """
        new_items = []
        for item in self.items:
            if item != '':
                new_items.append(item.strip())
        self.combo_box.clear()
        self.combo_box.addItems(new_items)

        if len(self.items) != 0:
            self.combo_box.setPlaceholderText(self.items[0])
        else:
            self.combo_box.setPlaceholderText("...")
        self.clear()
