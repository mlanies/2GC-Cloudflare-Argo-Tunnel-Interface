import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton, \
    QScrollArea, QHBoxLayout


class RssItem(QWidget):
    print(4)
    def __init__(self, title, date, parent = None):
        super(RssItem, self).__init__(parent)
        self.initWidget(title, date)

    def initWidget(self, title, date):
        title = QLabel(title)
        date = QLabel(date)
        titleBox = QHBoxLayout()
        titleBox.addWidget(title)
        titleBox.addWidget(date)
        self.setLayout(titleBox)

class ItemsList(QWidget):
    print(3)
    def __init__(self, items, parent=None):
        super(ItemsList, self).__init__(parent)
        self.initWidget(items)

    def initWidget(self, items):
        listBox = QVBoxLayout(self)
        self.setLayout(listBox)

        scroll = QScrollArea(self)
        listBox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)

        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        for item in items:
            scrollLayout.addWidget(item)
        scroll.setWidget(scrollContent)

class MainApp(QApplication):
    def __init__(self, args):
        print(1)
        super(MainApp, self).__init__(args)
        self.addWidgets()
        self.exec_()

    def addWidgets(self):
        self.window = MainWindow()


class MainWindow(QMainWindow):
    def __init__(self):
        print(2)
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage("ok")
        self.resize(640, 480)
        self.setWindowTitle("Smart Rss")
        items=[]
        for x in range(0, 5):
            items.append(RssItem("Title no %s" % x, "2000-1-%s" %x))
        self.setCentralWidget(ItemsList(items))
        self.show()

if __name__ == '__main__':
    app =MainApp(sys.argv)

# В этом примере размер главного окна увеличен до 400x300, чтобы было больше места для контента, и прокрутка должна появиться, если блоки информации не помещаются на экран.





