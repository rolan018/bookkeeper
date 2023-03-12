from PySide6 import QtWidgets


class LabelLine(QtWidgets.QWidget):
    """
    Input field
    """

    def __init__(self,
                 label_text: str,
                 place_holder: str,
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
        self.layout.addWidget(self.name, stretch=5)

    def clear(self):
        self.name.setText(self.place_holder)

    def text(self):
        return self.name.text()