"""
    Класс MainView представляет главное окно приложения 2GC: Server Manager.
В данном классе представлен внешний вид главного окна приложения,а так же события взаимодействия пользователя с ним.

Class:
    MainView(QMainWindow)

See Also:
    open_website: Функция для открытия сайта в браузере
    Styles: Класс в котором описанны все стили данного приложения.
    Switch, RoundedButton: Кастомные кнопки, используемые в приложении.
"""


from PyQt5.QtGui import QCursor, QIcon, QMouseEvent
from PyQt5.QtCore import QRect, Qt, QEvent, pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMenu, QLabel, QLineEdit
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QSizePolicy, QSystemTrayIcon, QToolTip

from win.views.buttons import Switch, RoundedButton
from .style import Styles
from win.utils import open_website


class MainView(QMainWindow):
    """
        Класс MainView представляет главное окно приложения 2GC: Server Manager.

    ...

    Attributes:
    -----------
        :cvar: open_connect (pyqtSignal): Сигнал, испускаемый при открытии соединения.
        :cvar: open_window (bool): Флаг, указывающий, открыто ли окно.
        :cvar: total_state (bool): Флаг, представляющий общее состояние приложения.

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
        _set_icon(): Метод создает иконку приложения.
        _set_trey_icon(): Метод создает иконку в трее и задает ей тул тип.
        _set_tray_menu(): Устанавливает контекстное меню для системного трея.
        _set_position(): Устанавливает позицию главного окна приложения в правой нижнем углу экрана.
        _set_structure(): Устанавливает структуру главного окна приложения и вызывает методы для отрисовки элементов.

        _set_header(): Задает стили, отступы и логотип в верхней части приложения.
        _set_logo_style(): Устанавливает стили, отступы и параметры Логотипа.
        _set_body(): Задает стили, отступы, очередность расположения элементов в основной части приложения.
        _set_bottom(): Задает стили, отступы, очередность расположения элементов в нижней части приложения.

        _empty_click(): Обработчик клика на switсh кнопку при отсутствии url.
    Private:

        __exit_application(): Скрывает значок в системном лотке, и корректно завершает приложение.

    See Also
    --------
        Класс является представление главного окна в MVC архитектуре.
    Основная логика приложения описанна в классе Controller


    Examples
    --------
        version = "2.0.0"
        site_url = "https://2gc.io/"
        url_views = "2gc.io"

        main_view = MainView(version, url_views, site_url)
        main_view.show()

    """

    open_connect = pyqtSignal(bool)
    open_window = True
    total_state = False

    def __init__(self, version: str, url_views: str, site_url: str):
        """
            Инициализирует экземпляр класса MainView.

        :param: version (str): Версия приложения.
        :param: url_views (str): URL представлений приложения.
        :param: site_url (str): URL сайта.
        """
        super().__init__()
        self.tray_icon = QSystemTrayIcon(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("2GC: Server Manager")
        self.setMinimumSize(280, 180)  # minimal size of window, чтобы не баловались
        self.resize(280, 180)

        # widget
        self.dom_widget = QWidget(self)
        self.top_widget = QWidget(self)
        self.body_widget = QWidget(self)
        self.bottom_widget = QWidget(self)

        # layout
        self.main_layout = QVBoxLayout(self.dom_widget)
        self.body_form_layout = QHBoxLayout(self.body_widget)
        self.bottom_layout = QHBoxLayout(self.bottom_widget)

        # menu
        self.tray_menu = QMenu(self)

        # label
        self.logo_label = QLabel("2GC", self.top_widget)
        self.connect_label = QLabel(self)
        self.version_label = QLabel(f"2GC FREE v{version}", self)
        self.site_link = QLabel(url_views, self)

        # icon
        self.rdp_off = QIcon('images/connect_icon_off.png')
        self.rdp_on = QIcon('images/connect_icon_on.png')
        self.dgc_icon = QIcon('images/trey_icon.ico')
        self.dgc_png = QIcon('images/trey_icon.png')

        # line edit
        self.url_input = QLineEdit(self.body_widget)

        # buttons
        self.switch_button = Switch("test", "test", track_radius=13, thumb_radius=11, width_size=4)
        self.close_button = RoundedButton(self)

        # style
        self.style = Styles()

        # ivar
        self.site_url = site_url
        self.init_ui()

    def init_ui(self) -> None:
        """
        Инициализация пользовательского интерфейса.

        Вызывает необходимые методы для установки иконки, регистрации в трее, меню, положения и структуры окна.

        :return: None
        """
        self._set_icon()
        self._set_trey_icon()
        self._set_tray_menu()
        self._set_position()
        self._set_structure()

    def _set_icon(self) -> None:
        """
            Метод создает иконку приложения
        :return: None
        """
        self.setWindowIcon(self.dgc_icon)

    def _set_trey_icon(self) -> None:
        """
        Метод создает иконку в трее и задает ей тул тип.
        """
        self.tray_icon.setIcon(self.dgc_png)
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip('2GC: Server Manager')

    def _set_tray_menu(self) -> None:
        """
            Устанавливает контекстное меню для системного трея.

        Данный метод добавляет действие "Выход" в контекстное меню системного трея,
        которое при выборе вызывает метод self.__exit_application.
        Затем он устанавливает контекстное меню для системного трея и делает его видимым.
        :return: None
        """
        self.tray_menu.addAction("Выход", self.__exit_application)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def _set_position(self) -> None:
        """
            Устанавливает позицию главного окна приложения в правой нижнем углу экрана.

        :return: None
        """
        desktop = QDesktopWidget().availableGeometry()
        window_rect = self.frameGeometry()
        x = desktop.width() - window_rect.width()
        y = desktop.height() - window_rect.height()
        self.move(x, y - 30)

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
            Устанавливает стили, отступы и параметры Логотипа.

        :return: None
        """
        self.logo_label.setStyleSheet(self.style.to_logo())
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.logo_label.setContentsMargins(0, 10, 0, 10)

    def _set_body(self) -> None:
        """
            Задает стили, отступы, очередность расположения элементов в основной части приложения.

        :return: None
        """
        self.connect_label.setPixmap(self.rdp_off.pixmap(50, 50))
        self.url_input.setStyleSheet(self.style.to_input())

        self.body_widget.setStyleSheet(self.style.to_body())
        self.body_widget.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addWidget(self.body_widget, 30)

        self.body_form_layout.addWidget(self.url_input)
        self.body_form_layout.addWidget(self.switch_button)
        self.body_form_layout.addWidget(self.connect_label)
        self.body_form_layout.addWidget(self.connect_label)

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

    def __exit_application(self) -> None:
        """
            Скрывает значок в системном лотке, и корректно завершает приложение.

        :return: None
        """
        self.tray_icon.hide()
        QApplication.quit()

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
            return super().eventFilter(watched, event)

        except Exception as ex:
            print(ex)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
            Переопределённый обработчик события нажатия кнопки мыши.

        Если нажата левая кнопка мыши, и курсор находится над меткой "connect_label", если включено общее состояние
        (total_state), генерируется сигнал открытия соединения (open_connect).

        В противном случае устанавливается флаг для перемещения окна и запоминается текущая позиция,
        а курсор изменяется на изображение открытой руки.

        :param event: (QMouseEvent) Событие нажатия кнопки мыши.
        :return: None
        """
        if event.button() == Qt.LeftButton:
            if self.connect_label.underMouse():
                if self.total_state:
                    self.open_connect.emit(True)
            else:
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

    def _empty_click(self) -> None:
        """
            Обработчик клика на switсh кнопку при отсутствии url.

        Сбрасывает кнопку переключения и устанавливает подсказку для ввода URL.

        :return: None
        """
        self.switch_button.reset_button()
        self.url_input.setPlaceholderText("введите URL")
        QToolTip.showText(self.url_input.mapToGlobal(self.url_input.rect().bottomLeft()),
                          "URL не должен быть пустым", self.url_input, QRect(), 3000)


