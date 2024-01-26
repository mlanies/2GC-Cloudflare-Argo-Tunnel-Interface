from PyQt5.QtWidgets import QPushButton


class RoundedButton(QPushButton):
    def __init__(self, parent=None):
        super(RoundedButton, self).__init__(parent)
        self.setFixedSize(20, 20)
        self.parent = parent
        self.setStyleSheet(
            "QPushButton {"
            "   background-color: #555555; "
            "   border-radius: 10px; "
            "   border: 1px solid #000000; "  
            "   color: white; "
            "}"
        )
        self.clicked.connect(self.close_application)

    def enterEvent(self, event):
        # Изменение цвета при наведении
        self.setStyleSheet(
            "background-color: #f3645c; "
            "border-radius: 10px; "
            "border: 1px solid #808080; " 
            "color: white;"
        )

    def leaveEvent(self, event):
        self.setStyleSheet(
            "background-color: #555555; "
            "border-radius: 10px; "
            "border: 1px solid #000000; "  
            "color: white;"
        )
        event.accept()

    def close_application(self):
        try:
            self.parent.open_window = False
            self.parent.close()
        except Exception as ex:
            print(ex)

