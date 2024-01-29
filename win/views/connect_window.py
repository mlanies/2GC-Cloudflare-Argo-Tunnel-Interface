"""
    Класс Connector представляет окно c опциями для подключения к удаленному рабочему столу.
В данном классе представлен внешний вид дополнительного окна приложения,
а так же события взаимодействия пользователя с ним.

Class:
    Connector(QMainWindow)

See Also:
    open_website: Функция для открытия сайта в браузере
    Styles: Класс в котором описанны все стили данного приложения.
    RoundedButton: Кастомная кнопка, используемые в приложении.
"""

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QEvent
from PyQt5.QtGui import QCursor, QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, \
    QCheckBox, QSizePolicy, QDesktopWidget

from win.views.buttons import RoundedButton
from win.views.style import Styles
from win.utils import open_website


class Connector(QMainWindow):
    """
        Класс Connector представляет окно c опциями для подключения к удаленному рабочему столу.

    ...

    Attributes:
    -----------
        :cvar: data_sent (pyqtSignal): Сигнал, для передачи данных пользователя.

    Parameters
        -----------
        :ivar: version (str): Версия приложения.
        :ivar: url_views (str): URL представлений приложения.
        :ivar: site_url (str): URL сайта.

    Methods:
    -------
    Public:
        init_ui(): Инициализация пользовательского интерфейса.
        eventFilter(self, watched, event): Переопределённый метод для обработки событий фильтрации.
        mousePressEvent(self, event): Переопределённый обработчик события нажатия кнопки мыши
        mouseMoveEvent(self, event): Переопределённый обработчик события перемещения мыши.
        mouseReleaseEvent(self, watched, event): Переопределённый обработчик события отпускания кнопки мыши.

    Protect:
        _set_position(): Устанавливает позицию главного окна приложения в правой нижнем углу экрана.
        _set_structure(): Устанавливает структуру главного окна приложения и вызывает методы для отрисовки элементов.

        _set_header(): Задает стили, отступы и логотип в верхней части приложения.
        _set_logo_style(): Устанавливает стили, отступы и параметры Логотипа.
        _set_body(): Задает стили, отступы, очередность расположения элементов в основной части приложения.
        _set_bottom(): Задает стили, отступы, очередность расположения элементов в нижней части приложения.


    See Also
    --------
        Класс является представление побочного окна в MVC архитектуре.
    Основная логика приложения описанна в классе Controller

    """
    data_sent = pyqtSignal(str, str, str, bool)
    def __init__(self, version: str, url_views: str, site_url: str):
        """
            Инициализирует экземпляр класса MainView.

        :param: version (str): Версия приложения.
        :param: url_views (str): URL представлений приложения.
        :param: site_url (str): URL сайта.
        """
        # application settings
        super().__init__()
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

        # label
        self.logo_label = QLabel("2GC", self.top_widget)
        self.connect_label = QLabel(self)
        self.version_label = QLabel(f"2GC FREE v{version}", self)
        self.site_link = QLabel(url_views, self)

        self.user_name_label = QLabel("Пользователь")
        self.password_label = QLabel("Пароль")
        self.domain_name_label = QLabel("Домен")
        self.save_text_label = QLabel("Сохранить")

        # line edit
        self.user_name_input = QLineEdit(self.body_widget)
        self.password_input = QLineEdit(self.body_widget)
        self.domain_name_input = QLineEdit(self.body_widget)

        # buttons
        self.connect_btn = QPushButton("Подключиться", self)
        self.close_button = RoundedButton(self)

        # check box
        self.save_checkbox = QCheckBox(self)

        self.user_name = ""
        self.domain_name = ""
        self.site_url = site_url

        self.style = Styles()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Инициализация пользовательского интерфейса.

        Вызывает необходимые методы для установки положения и структуры окна.

        :return: None
        """
        self._set_position()
        self._set_structure()

    def set_user_info(self, user_info: dict) -> None:
        """
            Устанавливает информацию о пользователе.

        :param: user_info: (dict) Словарь с информацией о пользователе.
        :return: None
        """
        self.user_name = user_info.get("login")
        self.domain_name = user_info.get("domain_name")
        self.user_name_input.setText(self.user_name)
        self.domain_name_input.setText(self.domain_name)

    def _set_structure(self) -> None:
        """
            Устанавливает структуру главного окна приложения и вызывает методы для отрисовки элементов.

        :return: None
        """
        self.setCentralWidget(self.dom_widget)
        self.close_button.move(self.width() - 25, 5)

        self._set_header()
        self._set_body()
        self._set_bottom()

    def _set_header(self) -> None:
        """
            Задает стили, отступы и логотип в верхней части приложения.

        :return: None
        """
        self._set_logo_style()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.logo_label)

        self.top_widget.resize(self.width(), 30)
        self.top_widget.setStyleSheet(self.style.to_transparent_widget())
        self.top_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def _set_logo_style(self) -> None:
        """
            Устанавливает стили и настройки для виджета Логотипа.

        :return: None
        """
        self.logo_label.setStyleSheet(self.style.to_logo())
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.logo_label.setContentsMargins(0, 10, 0, 10)

    def _set_body(self):
        self.body_widget.setContentsMargins(15, 0, 15, 0)
        self.body_widget.setStyleSheet(f"background-color: #393939;")
        self.main_layout.addWidget(self.body_widget, 150)


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

    def _set_bottom(self) -> None:
        """
            Задает стили, отступы, очередность расположения элементов в нижней части приложения.

        :return: None
        """
        self.bottom_widget.setStyleSheet(self.style.to_bottom())
        self.version_label.setStyleSheet(self.style.to_version_label())
        self.site_link.setStyleSheet(self.style.write_color())

        self.site_link.setCursor(Qt.PointingHandCursor)
        self.site_link.installEventFilter(self)

        self.bottom_layout.addWidget(self.version_label)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.site_link)

        self.main_layout.addWidget(self.bottom_widget, 15)

    def _set_position(self) -> None:
        """
            Устанавливает позицию виджета по центру экрана.

        :return: None
        """
        center = QDesktopWidget().availableGeometry().center()
        self.move(center.x() - self.frameSize().width() // 2, center.y() - self.frameSize().height() // 2)

    def close_window(self) -> None:
        """
            Очищает поле ввода пароля, и закрывает окно.

        :return: None
        """
        self.password_input.setText('')
        self.close()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """
                Переопределённый метод для обработки событий фильтрации.
        Отлавливает событие нажатия на ссылку, и открывает веб-сайт в браузере.

        :param: watched: (QObject) Объект, на котором отслеживаются события фильтрации.
        :param: event: (QEvent) Событие, которое отлавливается фильтром.

        :return: (bool): True, если событие обработано, False в противном случае.
        """
        try:
            if watched == self.site_link and event.type() == QEvent.MouseButtonPress:
                open_website(self.site_url)
                return True
            return super(Connector, self).eventFilter(watched, event)

        except Exception as ex:
            print(ex)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
            Переопределённый обработчик события нажатия кнопки мыши.

        При нажатии левой кнопки мыши устанавливает флаг `moveFlag` в значение True,
        сохраняет текущую позицию относительно глобальных координат и устанавливает курсор в вид руки.

        :param event: (QMouseEvent) Событие нажатия кнопки мыши.
        :return: None
        """
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
            Переопределённый обработчик события перемещения мыши.

        Если нажата левая кнопка мыши и установлен флаг перемещения (moveFlag),
        окно перемещается в соответствии с текущим положением мыши и сохраненной позицией.

        :param event: (QMouseEvent) Событие перемещения мыши.
        :return: None
        """
        if Qt.LeftButton and self.moveFlag:
            self.move(event.globalPos() - self.movePosition)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
            Переопределённый обработчик события отпускания кнопки мыши.
        Сбрасывает флаг перемещения, возвращает курсор в обычное состояние.

        :param event: (QMouseEvent) Событие отпускания кнопки мыши.
        :return: None
        """
        self.moveFlag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
            Переопределённый метод обрабатывающий событие нажатия клавиши.
        Вызывает функцию send_data при нажатии клавиши Enter.

        :param event: (QKeyEvent) Событие нажатия клавиши.
        :return: None
        """
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.send_data()
        else:
            super().keyPressEvent(event)

    def send_data(self) -> None:
        """
            Отправляет введенные данные, если заполнены обязательные поля.

        Получает значения из полей ввода для имени пользователя, пароля и доменного имени. Если введены имя пользователя
        и пароль, отправляет сигнал `data_sent` с передачей введенных данных и состояния флажка сохранения пароля.
        Затем вызывает метод для закрытия текущего окна.

        В случае, если не введено имя пользователя,
        устанавливает стиль ошибки и отображает подсказку. Аналогично для поля пароля.

        :return: None
        """
        user_name = self.user_name_input.text()
        password = self.password_input.text()
        domain_name = self.domain_name_input.text()

        if user_name and password:
            self.data_sent.emit(user_name, password, domain_name, self.save_checkbox.isChecked())
            self.close_window()

        elif not user_name:
            self.user_name_input.setStyleSheet(self.style.to_input_error())
            self.user_name_input.setPlaceholderText("Поле не должно быть пустым")

        if not password:
            self.password_input.setStyleSheet(self.style.to_input_error())
            self.password_input.setPlaceholderText("Поле не должно быть пустым")

    def handle_input(self) -> None:
        """
            Обрабатывает введенные данные пользователем.

        Получает значения из полей ввода для имени пользователя и пароля.
        При наличии символов в полях пользователя или пароля, возвращает им обычный вид.

        :return: None
        """
        user_name = self.user_name_input.text()
        password = self.password_input.text()
        if user_name:
            self.user_name_input.setStyleSheet(self.style.to_input())
        if password:
            self.password_input.setStyleSheet(self.style.to_input())

