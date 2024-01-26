import webbrowser

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QEvent
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMenu, QLabel, QHBoxLayout, QLineEdit, QPushButton, \
    QCheckBox, QSizePolicy, QDesktopWidget

from win.views.buttons import RoundedButton
from win.views.style import Styles


class Connector(QMainWindow):
    dataSent = pyqtSignal(str, str, str, bool)
    server_states = {}
    process = {}
    server_port = {}
    version = "2.0.0"
    site_url = "https://2gc.io/"
    url_views = "2gc.io"

    def __init__(self):
        super().__init__()
        # application settings
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("2GC: Server Manager")
        self.setMinimumSize(230, 180)  # minimal size of window, чтобы не баловались
        self.resize(230, 320)

        # widget
        self.dom_widget = QWidget(self)
        self.top_widget = QWidget(self)
        self.body_widget = QWidget(self)
        self.bottom_widget = QWidget(self)

        # layout
        self.main_layout = QVBoxLayout(self.dom_widget)
        self.body_form_layout = QVBoxLayout(self.body_widget)
        self.bottom_layout = QHBoxLayout(self.bottom_widget)
        self.save_layout = QHBoxLayout()

        # menu
        self.tray_menu = QMenu(self)

        # label
        self.logo_label = QLabel("2GC", self.top_widget)
        self.version_label = QLabel(f"2GC FREE v{self.version}", self)
        self.site_link = QLabel(self.url_views, self)

        self.user_name_label = QLabel("Пользователь")
        self.password_label = QLabel("Пароль")
        self.domain_name_label = QLabel("Домен")
        self.save_text_label = QLabel("Сохранить")

        # line edit
        self.user_name_input = QLineEdit(self.body_widget)
        self.password_input = QLineEdit(self.body_widget)
        self.domain_name_input = QLineEdit(self.body_widget)

        self.connect_btn = QPushButton("Подключиться", self)

        self.user_name = ""
        self.domain_name = ""

        self.save_checkbox = QCheckBox(self)
        self.style = Styles()

        self.init_ui()

    def init_ui(self):
        self.set_position()
        self.set_structure()

    def set_user_info(self, user_info):
        self.user_name = user_info.get("login")
        self.domain_name = user_info.get("domain_name")
        print(self.user_name)
        print(self.domain_name)
        self.user_name_input.setText(self.user_name)
        self.domain_name_input.setText(self.domain_name)

    def set_structure(self, ):
        self.setCentralWidget(self.dom_widget)


        self.__set_header()
        self.__set_body()
        self.__set_bottom()
        self.main_layout.addWidget(self.bottom_widget, 15)

    def __set_header(self):
        self.__set_logo_style()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.top_widget.resize(self.width(), 30)
        self.top_widget.setStyleSheet(f"background-color: rgba(255,255,255, 0);")
        self.create_rounded_button()
        self.top_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(self.logo_label)

    def __set_logo_style(self) -> None:
        """
            Устанавливает стили и настройки для виджета Логотипа.

        :return: None
        """
        self.logo_label.setStyleSheet(self.style.to_logo())
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.logo_label.setContentsMargins(0, 10, 0, 10)

    def __set_icons(self):
        self.icon_label.setStyleSheet(self.style.to_logo())
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.icon_label.setContentsMargins(0, 10, 0, 10)
        return self.icon_label

    def create_rounded_button(self):
        button = RoundedButton(self)
        button.move(self.width() - 25, 5)
        return button

    def __set_body(self):
        self.body_widget.setContentsMargins(15, 0, 15, 0)
        self.body_widget.setStyleSheet(f"background-color: #393939;")
        self.main_layout.addWidget(self.body_widget, 150)

        self.__set_input_text()

        self.user_name_input.setStyleSheet(self.style.to_input())
        if self.user_name:
            self.user_name_input.setText(self.user_name)
        else:
            self.user_name_input.setPlaceholderText("Admin")
        self.password_input.setStyleSheet(self.style.to_input())
        self.password_input.setEchoMode(QLineEdit.Password)
        self.domain_name_input.setStyleSheet(self.style.to_input())
        if self.domain_name:
            self.domain_name_input.setText(self.domain_name)
        else:
            self.domain_name_input.setPlaceholderText("Workspace")

        self.user_name_input.textChanged.connect(self.handle_input)
        self.domain_name_input.textChanged.connect(self.handle_input)

        self.user_name_label.setStyleSheet(self.style.to_input_label())

        self.password_label.setStyleSheet(self.style.to_input_label())
        self.domain_name_label.setStyleSheet(self.style.to_input_label())

        self.body_form_layout.addWidget(self.user_name_label)
        self.body_form_layout.addWidget(self.user_name_input)

        self.body_form_layout.addWidget(self.password_label)
        self.body_form_layout.addWidget(self.password_input)

        self.body_form_layout.addWidget(self.domain_name_label)
        self.body_form_layout.addWidget(self.domain_name_input)

        self.save_text_label.setStyleSheet(self.style.to_input_label())
        self.save_layout.addWidget(self.save_checkbox)
        self.save_layout.addWidget(self.save_text_label)
        self.save_layout.addStretch()

        self.save_checkbox.setToolTip("Сохранить логин и домен")
        self.save_text_label.setToolTip("Сохранить логин и домен")

        self.body_form_layout.addLayout(self.save_layout)

        self.connect_btn.setStyleSheet(self.style.to_connect_btn())
        self.connect_btn.clicked.connect(self.send_data)

        self.body_form_layout.addWidget(self.connect_btn)

        self.setCursor(QCursor(Qt.PointingHandCursor))

    def __set_input_text(self):
        ...
        # try:
        #     url = self.sqlite_db.get_last_url()
        #     if url:
        #         self.user_name_input.setText(url[0][0])
        #     else:
        #         self.user_name_input.setPlaceholderText("введите URL")
        # except Exception as ex:
        #     FileLogger.log_warning(ex)
        #     self.user_name_input.setPlaceholderText("введите URL")

    def __set_bottom(self):

        self.bottom_widget.setStyleSheet(self.style.to_bottom())
        try:
            self.version_label.setStyleSheet("color: white; font-size: 9px;")

            self.site_link.setStyleSheet("color: white;")
            self.site_link.setCursor(Qt.PointingHandCursor)
            self.site_link.installEventFilter(self)

            # Добавьте метку в макет
            self.bottom_layout.addWidget(self.version_label)
            self.bottom_layout.addStretch()
            self.bottom_layout.addWidget(self.site_link)
        except Exception as ex:
            print(ex)

    def set_position(self) -> None:
        """
        Устанавливает позицию виджета по центру экрана.
        """
        center = QDesktopWidget().availableGeometry().center()
        self.move(center.x() - self.frameSize().width() // 2, center.y() - self.frameSize().height() // 2)

    def exit_application(self) -> None:
        try:
            self.password_input.setText('')
            self.close()
        except Exception as ex:
            print(ex)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """
            Фильтр событий для виджета. Обрабатывает события клика по ссылке на сайт.

        :param watched: (QObject) Виджет, отслеживаемый фильтром событий.
        :param event: (QEvent) Событие, которое обрабатывается.
        :return: True, если событие было обработано, в противном случае - None.
         """
        try:
            if watched == self.site_link and event.type() == QEvent.MouseButtonPress:
                self.open_website()
                return True
            return super(Connector, self).eventFilter(watched, event)

        except Exception as ex:
            print(ex)

    def mousePressEvent(self, event) -> None:
        """
            Обрабатывает событие нажатия кнопки мыши.
        Перемещает виджет при зажатой левой кнопке мыши.

        :param event: Событие нажатия кнопки мыши.
        :type event: QMouseEvent
        """
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        try:
            if Qt.LeftButton and self.moveFlag:
                self.move(event.globalPos() - self.movePosition)
            super().mouseMoveEvent(event)
        except Exception as ex:
            print(f'255{ex=}')

    def mouseReleaseEvent(self, event) -> None:
        """
            Обрабатывает событие перемещения мыши.
            Перемещает виджет при зажатой левой кнопке мыши.

        :param event: Событие перемещения мыши.
        :type event: QMouseEvent
        """
        try:
            self.moveFlag = False
            self.setCursor(QCursor(Qt.ArrowCursor))
            super().mouseReleaseEvent(event)
        except Exception as ex:
            print(f'267{ex=}')

    def keyPressEvent(self, event):
        """
            Обрабатывает событие нажатия клавиши.
        Вызывает функцию send_data при нажатии клавиши Enter.

        :param event: Событие нажатия клавиши.
        :type event: QKeyEvent
        """
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.send_data()
        else:
            super().keyPressEvent(event)

    def send_data(self):
        user_name = self.user_name_input.text()
        password = self.password_input.text()
        domain_name = self.domain_name_input.text()

        if user_name and password:
            self.dataSent.emit(user_name, password, domain_name, self.save_checkbox.isChecked())
            self.exit_application()

        elif not user_name:
            self.user_name_input.setStyleSheet(self.style.to_input_error())
            self.user_name_input.setPlaceholderText("Поле не должно быть пустым")

        if not password:
            self.password_input.setStyleSheet(self.style.to_input_error())
            self.password_input.setPlaceholderText("Поле не должно быть пустым")

    def handle_input(self):
        user_name = self.user_name_input.text()
        password = self.password_input.text()
        if user_name:
            self.user_name_input.setStyleSheet(self.style.to_input())

        if password:
            self.password_input.setStyleSheet(self.style.to_input())

    def open_website(self):
        webbrowser.open(self.site_url)