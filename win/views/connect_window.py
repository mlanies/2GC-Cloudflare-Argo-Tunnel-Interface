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
from PyQt5.QtGui import QCursor, QKeyEvent, QMouseEvent, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, \
    QCheckBox, QSizePolicy, QDesktopWidget, QLayout

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
        :cvar: update_settings (pyqtSignal): Сигнал, для передачи измененных настроек.

    Parameters
        -----------
        :ivar: version (str): Версия приложения.
        :ivar: url_views (str): URL представлений приложения.
        :ivar: site_url (str): URL сайта.

    Methods:
    -------
    Public:
        clear_vbox(vbox): Полностью очищает преданный лайаут.
        close_window(): Очищает поле ввода пароля, и закрывает окно.
        handle_input(): Обрабатывает введенные данные пользователем.
        send_data(): Отправляет введенные данные, если заполнены обязательные поля.
        repaint_body(): Метод для перерисовки центрального виджета.
        on_checkbox_changed(): Отлавливает изменения чекбоксов в окне настроек, и отправляет сигнал с этим изменением.
        eventFilter(watched, event): Переопределённый метод для обработки событий фильтрации.
        keyPressEvent(event): Переопределённый метод обрабатывающий событие нажатия клавиши.
        mousePressEvent(event): Переопределённый обработчик события нажатия кнопки мыши
        mouseMoveEvent(event): Переопределённый обработчик события перемещения мыши.
        mouseReleaseEvent(watched, event): Переопределённый обработчик события отпускания кнопки мыши.

        main_body_create_widgets(): Создает все виджеты необходимые главному окну.
        settings_body_create_widgets(): Создает все виджеты необходимые окну настроек.


    Protect:


        _set_position(): Устанавливает позицию главного окна приложения в правой нижнем углу экрана.
        _set_structure(): Устанавливает структуру главного окна приложения и вызывает методы для отрисовки элементов.
        _set_style_widget():  Добавляет стили и отступы части элементов.
        _set_header(): Задает стили, отступы и логотип в верхней части приложения.
        _set_logo_style(): Устанавливает стили, отступы и параметры Логотипа.
        _set_main_body(): Задает очередность расположения элементов в основной части приложения.
        _set_settings_body(): Задает очередность расположения элементов в основной части приложения, в окне настроек.
        _set_bottom(): Задает стили, отступы, очередность расположения элементов в нижней части приложения.


    See Also
    --------
        Класс является представление побочного окна в MVC архитектуре.
    Основная логика приложения описанна в классе Controller

    """
    data_sent = pyqtSignal(str, str, str, bool)
    update_settings = pyqtSignal(str, bool)

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
        self.setMinimumSize(230, 350)  # minimal size of window, чтобы не баловались
        self.resize(230, 350)

        # widget
        self.dom_widget = QWidget(self)
        self.top_widget = QWidget(self)
        self.body_widget = QWidget(self)
        self.bottom_widget = QWidget(self)

        # layout
        self.main_layout = QVBoxLayout(self.dom_widget)
        self.body_form_layout = QVBoxLayout(self.body_widget)
        self.bottom_layout = QHBoxLayout(self.bottom_widget)
        self.save_layout = None
        self.settings_connect_layout = None

        self.printer_layout = None
        self.disks_layout = None
        self.sound_layout = None
        self.wallpapers_layout = None
        self.all_monitors_layout = None

        # label
        self.logo_label = QLabel("2GC", self.top_widget)
        self.settings_label = None
        self.version_label = QLabel(f"2GC FREE v{version}", self)
        self.site_link = QLabel(url_views, self)

        self.user_name_label = None
        self.password_label = None
        self.domain_name_label = None
        self.save_text_label = None

        self.redirecting_the_printer_label = None
        self.redirecting_the_disks_label = None
        self.sound_from_remote_desktop_label = None
        self.desktop_wallpapers_label = None
        self.use_all_monitors_label = None

        # line edit
        self.user_name_input = None
        self.password_input = None
        self.domain_name_input = None

        # buttons
        self.connect_btn = None
        self.apply_btn = None
        self.close_button = RoundedButton(self)

        # check box
        self.save_checkbox = None
        self.redirecting_the_printer_checkbox = None
        self.redirecting_the_disks_checkbox = None
        self.sound_from_remote_desktop_checkbox = None
        self.desktop_wallpapers_checkbox = None
        self.use_all_monitors_checkbox = None

        # icon
        self.settings_buttons = QIcon('images/settings_buttons.png')

        self.user_name = ""
        self.domain_name = ""
        self.main_body = True
        self.site_url = site_url
        self.settings_data = dict()

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
        self._set_style_widget()

    def _set_style_widget(self) -> None:
        """
            Добавляет стили и отступы части элементов.

        :return: None
        """
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_label.setContentsMargins(0, 10, 0, 10)
        self.body_widget.setContentsMargins(15, 0, 15, 0)

        self.logo_label.setStyleSheet(self.style.to_logo())
        self.body_widget.setStyleSheet(self.style.to_body())
        self.bottom_widget.setStyleSheet(self.style.to_bottom())
        self.version_label.setStyleSheet(self.style.to_version_label())
        self.site_link.setStyleSheet(self.style.write_color())

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
        self.main_layout.addWidget(self.body_widget, 150)
        self._set_main_body()
        self._set_bottom()

    def _set_header(self) -> None:
        """
            Задает стили, отступы и логотип в верхней части приложения.

        :return: None
        """
        self._set_logo_style()

        self.main_layout.addWidget(self.logo_label)

        self.top_widget.resize(self.width(), 30)
        self.top_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def _set_logo_style(self) -> None:
        """
            Устанавливает стили и настройки для виджета Логотипа.

        :return: None
        """

        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def main_body_create_widgets(self) -> None:
        """
           Создает все виджеты необходимые главному окну.

        :return: None
        """
        self.save_layout = QHBoxLayout()
        self.settings_connect_layout = QHBoxLayout()

        self.settings_label = QLabel(self)

        self.user_name_label = QLabel("Пользователь")
        self.password_label = QLabel("Пароль")
        self.domain_name_label = QLabel("Домен")
        self.save_text_label = QLabel("Сохранить")

        self.user_name_input = QLineEdit()
        self.password_input = QLineEdit()
        self.domain_name_input = QLineEdit()

        self.connect_btn = QPushButton("Подключиться")

        self.save_checkbox = QCheckBox()

        self.settings_buttons = QIcon('images/settings_buttons.png')

    def settings_body_create_widgets(self) -> None:
        """
           Создает все виджеты необходимые окну настроек.

        :return: None
        """
        self.printer_layout = QHBoxLayout()
        self.disks_layout = QHBoxLayout()
        self.sound_layout = QHBoxLayout()
        self.wallpapers_layout = QHBoxLayout()
        self.all_monitors_layout = QHBoxLayout()

        self.redirecting_the_printer_label = QLabel("Перенаправление принтера")
        self.redirecting_the_disks_label = QLabel("Перенаправление дисков")
        self.sound_from_remote_desktop_label = QLabel("Звук с удаленного компьютера")
        self.desktop_wallpapers_label = QLabel("Отображение обоев удаленного компьютера")
        self.use_all_monitors_label = QLabel("Использовать все мониторы")

        self.redirecting_the_printer_label.setStyleSheet(self.style.write_color())
        self.redirecting_the_disks_label.setStyleSheet(self.style.write_color())
        self.sound_from_remote_desktop_label.setStyleSheet(self.style.write_color())
        self.desktop_wallpapers_label.setStyleSheet(self.style.write_color())
        self.desktop_wallpapers_label.setWordWrap(True)
        self.use_all_monitors_label.setStyleSheet(self.style.write_color())

        self.apply_btn = QPushButton("Применить")

        self.apply_btn.setStyleSheet(self.style.to_connect_btn())

        self.redirecting_the_printer_checkbox = QCheckBox()
        self.redirecting_the_printer_checkbox.setChecked(self.settings_data.get("printer", True))
        self.redirecting_the_printer_checkbox.stateChanged.connect(self.on_checkbox_changed)

        self.redirecting_the_disks_checkbox = QCheckBox()
        self.redirecting_the_disks_checkbox.setChecked(self.settings_data.get("disks", False))
        self.redirecting_the_disks_checkbox.stateChanged.connect(self.on_checkbox_changed)

        self.sound_from_remote_desktop_checkbox = QCheckBox()
        self.sound_from_remote_desktop_checkbox.setChecked(self.settings_data.get("sound", True))
        self.sound_from_remote_desktop_checkbox.stateChanged.connect(self.on_checkbox_changed)

        self.desktop_wallpapers_checkbox = QCheckBox()
        self.desktop_wallpapers_checkbox.setChecked(self.settings_data.get("desktop_wallpapers", True))
        self.desktop_wallpapers_checkbox.stateChanged.connect(self.on_checkbox_changed)

        self.use_all_monitors_checkbox = QCheckBox()
        self.use_all_monitors_checkbox.setChecked(self.settings_data.get("use_all_monitors", True))
        self.use_all_monitors_checkbox.stateChanged.connect(self.on_checkbox_changed)

        self.unsetCursor()

    def on_checkbox_changed(self) -> None:
        """
           Отлавливает изменения чекбоксов в окне настроек, и отправляет сигнал с этим изменением.

        :return: None
        """
        switch_dict = {
            self.redirecting_the_printer_checkbox: "printer",
            self.redirecting_the_disks_checkbox: "disks",
            self.sound_from_remote_desktop_checkbox: "sound",
            self.desktop_wallpapers_checkbox: "desktop_wallpapers",
            self.use_all_monitors_checkbox: "use_all_monitors"
        }
        checkbox = self.sender()
        settings_name = switch_dict[checkbox]
        new_settings_value = not self.settings_data[settings_name]
        self.settings_data[settings_name] = not new_settings_value

        self.update_settings.emit(settings_name, new_settings_value)

    def _set_settings_body(self) -> None:
        """
           Задает очередность расположения элементов в основной части приложения, в окне настроек.

        :return: None
        """
        self.settings_body_create_widgets()
        self.printer_layout.addWidget(self.redirecting_the_printer_checkbox)
        self.printer_layout.addWidget(self.redirecting_the_printer_label)
        self.printer_layout.addStretch()

        self.disks_layout.addWidget(self.redirecting_the_disks_checkbox)
        self.disks_layout.addWidget(self.redirecting_the_disks_label)
        self.disks_layout.addStretch()

        self.sound_layout.addWidget(self.sound_from_remote_desktop_checkbox)
        self.sound_layout.addWidget(self.sound_from_remote_desktop_label)
        self.sound_layout.addStretch()

        self.wallpapers_layout.addWidget(self.desktop_wallpapers_checkbox)
        self.wallpapers_layout.addWidget(self.desktop_wallpapers_label)
        self.wallpapers_layout.addStretch()

        self.all_monitors_layout.addWidget(self.use_all_monitors_checkbox)
        self.all_monitors_layout.addWidget(self.use_all_monitors_label)
        self.all_monitors_layout.addStretch()

        self.body_form_layout.addLayout(self.printer_layout)
        self.body_form_layout.addLayout(self.disks_layout)
        self.body_form_layout.addLayout(self.sound_layout)
        self.body_form_layout.addLayout(self.wallpapers_layout)
        self.body_form_layout.addLayout(self.all_monitors_layout)
        self.body_form_layout.addWidget(self.apply_btn)

        self.apply_btn.clicked.connect(self.repaint_body)
        self.apply_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.unsetCursor()

    def repaint_body(self) -> None:
        """
            Метод для перерисовки центрального виджета.
        Очищает его, и в зависимости от состояния отрисовывает нужный контент

        :return: None
        """
        try:
            self.clear_vbox(self.body_form_layout)
        except Exception as ex:
            print(ex)

        if self.main_body:
            self._set_settings_body()
        else:
            self._set_main_body()
        self.main_body = not self.main_body
        self.repaint()

    def clear_vbox(self, vbox: QLayout) -> None:
        """
            Полностью очищает преданный лайаут.

        :return: None
        """
        if vbox is not None:
            while vbox.count():
                item = vbox.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_vbox(item.layout())

    def _set_main_body(self) -> None:
        """
            Задает очередность расположения элементов в основной части приложения.

        :return: None
        """
        self.main_body_create_widgets()
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

        # Первая линия
        self.body_form_layout.addWidget(self.user_name_label)
        self.body_form_layout.addWidget(self.user_name_input)

        # Вторая линия
        self.body_form_layout.addWidget(self.password_label)
        self.body_form_layout.addWidget(self.password_input)

        # Третья линия
        self.body_form_layout.addWidget(self.domain_name_label)
        self.body_form_layout.addWidget(self.domain_name_input)

        # Четвертая линия
        self.save_text_label.setStyleSheet(self.style.to_input_label())
        self.save_layout.addWidget(self.save_checkbox)
        self.save_layout.addWidget(self.save_text_label)
        self.save_layout.addStretch()

        self.save_checkbox.setToolTip("Сохранить логин и домен")
        self.save_text_label.setToolTip("Сохранить логин и домен")

        self.body_form_layout.addLayout(self.save_layout)

        # Пятая линия
        self.connect_btn.setStyleSheet(self.style.to_connect_btn())
        self.connect_btn.clicked.connect(self.send_data)
        self.connect_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.settings_label.setPixmap(self.settings_buttons.pixmap(25, 25))
        self.settings_label.setMinimumWidth(30)
        self.settings_label.setCursor(QCursor(Qt.PointingHandCursor))

        self.settings_connect_layout.addWidget(self.connect_btn)
        self.settings_connect_layout.addWidget(self.settings_label)

        self.connect_btn.setMinimumWidth(150)

        self.body_form_layout.addLayout(self.settings_connect_layout)

        self.unsetCursor()

    def _set_bottom(self) -> None:
        """
            Задает стили, отступы, очередность расположения элементов в нижней части приложения.

        :return: None
        """
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
        try:
            if event.button() == Qt.LeftButton:
                if self.main_body:
                    if self.settings_label.underMouse():
                        self.repaint_body()
                    else:
                        self.moveFlag = True
                        self.movePosition = event.globalPos() - self.pos()
                        self.setCursor(QCursor(Qt.OpenHandCursor))
                else:
                    self.moveFlag = True
                    self.movePosition = event.globalPos() - self.pos()
                    self.setCursor(QCursor(Qt.OpenHandCursor))
            super().mousePressEvent(event)
        except Exception as ex:
            print(ex)

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
