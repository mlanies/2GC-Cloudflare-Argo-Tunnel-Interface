import os
import sys
import time
import random
import subprocess
import webbrowser

import psutil
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import QRect, Qt, QEvent, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMenu, QLabel, QLineEdit
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QSizePolicy, QSystemTrayIcon, QToolTip

from win.views.buttons import Switch, RoundedButton
from .style import Styles


class MainView(QMainWindow):
    open_connect = pyqtSignal(bool)
    radius = 15
    open_window = True
    total_state = False
    version = "2.0.0"
    site_url = "https://2gc.io/"
    url_views = "2gc.io"

    def __init__(self):
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
        self.version_label = QLabel(f"2GC FREE v{self.version}", self)
        self.site_link = QLabel(self.url_views, self)

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

        self.style = Styles()
        self.init_ui()

    def init_ui(self):

        self.set_icon()
        self.set_trey_icon()
        self.set_tray_menu() #
        self.set_position()
        self.set_structure()
        # self.tray_icon.activated.connect(self.trigger)

    def set_icon(self) -> None:
        """
        Метод создает иконку приложения
        :return: None
        """
        self.setWindowIcon(self.dgc_icon)

    def set_trey_icon(self) -> None:
        """
        Метод создает иконку в трее
        """
        self.tray_icon.setIcon(self.dgc_png)
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip('2GC: Server Manager')

    def set_tray_menu(self) -> None: # доделать
        """
        Устанавливает контекстное меню для системного трея.

        Данный метод добавляет действие "Выход" в контекстное меню системного трея, которое при выборе вызывает метод self.exit_application.
        Затем он устанавливает контекстное меню для системного трея и делает его видимым.
        :return: None
        """
        self.tray_menu.addAction("Выход", self.exit_application)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def set_position(self) -> None:
        """
        Устанавливает позицию главного окна приложения.

        :return: None
        """
        desktop = QDesktopWidget().availableGeometry()
        window_rect = self.frameGeometry()
        x = desktop.width() - window_rect.width()
        y = desktop.height() - window_rect.height()
        self.move(x, y - 30)

    def set_structure(self) -> None:
        """
        Устанавливает структуру главного окна приложения.

        :return: None
        """
        self.setCentralWidget(self.dom_widget)
        self.close_button.move(self.width() - 25, 5)

        self.__set_header()
        self.__set_body()
        self.__set_bottom()
        self.main_layout.addWidget(self.bottom_widget, 15)

    def __set_header(self) -> None:
        """
        Устанавливает верхнюю часть главного окна приложения.

        :return: None
        """
        self.__set_logo_style()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.top_widget.resize(self.width(), 30)

        self.top_widget.setStyleSheet(self.style.to_transparent_widget())
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

    def __set_body(self) -> None:
        """
            Настраивает тело виджета.

        :return: None
        """
        self.body_widget.setContentsMargins(0, 0, 0, 0)
        self.body_widget.setStyleSheet(self.style.to_body())
        self.main_layout.addWidget(self.body_widget, 30)
        self.url_input.setStyleSheet(self.style.to_input())
        # self.switch_button.clicked.connect(self.handle_switch_click)
        self.body_form_layout.addWidget(self.url_input)
        self.body_form_layout.addWidget(self.switch_button)
        self.connect_label.setPixmap(self.rdp_off.pixmap(50, 50))
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.body_form_layout.addWidget(self.connect_label)
        self.body_form_layout.addWidget(self.connect_label)

    def __set_bottom(self):
        self.bottom_widget.setStyleSheet(self.style.to_bottom())
        self.version_label.setStyleSheet(self.style.to_version_label())
        self.site_link.setStyleSheet(self.style.write_color())
        try:
            self.site_link.setCursor(Qt.PointingHandCursor)
            self.site_link.installEventFilter(self)

            # Добавьте метку в макет
            self.bottom_layout.addWidget(self.version_label)
            self.bottom_layout.addStretch()
            self.bottom_layout.addWidget(self.site_link)
        except Exception as ex:
            print(ex)

    def exit_application(self):
        self.tray_icon.hide()
        QApplication.quit()

    def eventFilter(self, watched, event):
        try:
            if watched == self.site_link and event.type() == QEvent.MouseButtonPress:
                self.open_website()
                return True
            return super().eventFilter(watched, event)

        except Exception as ex:
            print(ex)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            if self.connect_label.underMouse():
                # Клик произошел именно по self.connect_label
                print(1)
                if self.total_state:
                    self.open_connect.emit(True)

                    # self.open_mstsc()
            else:
                self.moveFlag = True
                self.movePosition = event.globalPos() - self.pos()
                self.setCursor(QCursor(Qt.OpenHandCursor))
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.moveFlag:
            self.move(event.globalPos() - self.movePosition)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.moveFlag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        super().mouseReleaseEvent(event)

    def empty_click(self):
        self.switch_button.reset_button()
        self.url_input.setPlaceholderText("введите URL")
        QToolTip.showText(self.url_input.mapToGlobal(self.url_input.rect().bottomLeft()),
                          "URL не должен быть пустым", self.url_input, QRect(), 3000)