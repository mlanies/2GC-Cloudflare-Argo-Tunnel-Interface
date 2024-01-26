from PyQt5.QtCore import QPropertyAnimation, QRectF, QSize, Qt, pyqtProperty
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QPen, QPainterPath, QBrush
from PyQt5.QtWidgets import QAbstractButton, QSizePolicy


class Switch(QAbstractButton):
    def __init__(self, app, title, track_radius=10, thumb_radius=8, parent=None, *, width_size=4):
        super().__init__(parent=parent)
        self.setCheckable(True)
        self.title = title
        self.app = app
        self.width_size = width_size
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._track_radius = track_radius
        self._thumb_radius = thumb_radius
        self.total_state = False
        self._margin = max(0, self._thumb_radius - self._track_radius)
        self._base_offset = max(self._thumb_radius, self._track_radius)
        self._end_offset = {
            True: lambda: self.width() - self._base_offset,
            False: lambda: self._base_offset,
        }
        self._offset = self._base_offset

        palette = self.palette()
        if self._thumb_radius > self._track_radius:
            gradient = QLinearGradient(0, 0, self.width(), 0)
            gradient.setColorAt(0, QColor("#FFA253"))  # Change the color here
            gradient.setColorAt(1, QColor("#FFBB7A"))  # Change the color here
            self._track_color = {
                True: gradient,
                False: palette.dark(),
            }
            self._thumb_color = {
                True: gradient,
                False: gradient,
            }
            self._text_color = {
                True: palette.highlightedText().color(),
                False: palette.dark().color(),
            }
            self._thumb_text = {
                True: '',
                False: '',
            }
            self._track_opacity = 0.5
        else:
            self._thumb_color = {
                True: palette.highlightedText(),
                False: QColor("#FFFFFF"),
            }
            self._track_color = {
                True: QColor("#008000"),
                False: QColor("#d00000"),  # задний фон при выключении
            }
            self._text_color = {
                True: QColor("#000000"),
                False: QColor("#ffffff"),
            }
            self._thumb_text = {
                True: '',
                False: '',
            }
            self._text_position = {
                True: 2.1,
                False: 2.4
            }
            self._track_opacity = 1

    @pyqtProperty(int)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()

    def sizeHint(self):  # pylint: disable=invalid-name
        return QSize(
            self.width_size * self._track_radius + 2 * self._margin,
            2 * self._track_radius + 2 * self._margin,
        )

    def setChecked(self, checked):
        super().setChecked(checked)
        self.offset = self._end_offset[checked]()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.offset = self._end_offset[self.isChecked()]()

    def paintEvent(self, event):  # pylint: disable=invalid-name, unused-argument
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)

        track_opacity = self._track_opacity
        thumb_opacity = 1.0
        text_opacity = 1.0
        if self.isEnabled():
            track_brush = self._track_color[self.isChecked()]
            thumb_brush = self._thumb_color[self.isChecked()]
            text_color = self._text_color[self.isChecked()]
        else:
            track_opacity *= 0.8
            track_brush = self.palette().shadow()
            thumb_brush = self.palette().mid()
            text_color = self.palette().shadow().color()

        p.setBrush(track_brush)
        p.setOpacity(track_opacity)
        p.drawRoundedRect(
            self._margin,
            self._margin,
            self.width() - 2 * self._margin,
            self.height() - 2 * self._margin,
            self._track_radius,
            self._track_radius,
        )
        p.setBrush(thumb_brush)
        p.setOpacity(thumb_opacity)
        p.drawEllipse(
            self.offset - self._thumb_radius,
            self._base_offset - self._thumb_radius,
            2 * self._thumb_radius,
            2 * self._thumb_radius,
        )
        p.setPen(text_color)
        p.setOpacity(text_opacity)
        font = p.font()
        font.setPixelSize(int(0.87 * self._thumb_radius))
        p.setFont(font)
        p.drawText(
            QRectF(
                self._margin,
                self._margin,
                self._text_position[self.isChecked()] * self._thumb_radius,
                2 * self._thumb_radius,
            ),
            Qt.AlignCenter,
            self._thumb_text[self.isChecked()],
        )

    def mouseReleaseEvent(self, event):  # pylint: disable=invalid-name
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            anim = QPropertyAnimation(self, b'offset', self)
            anim.setDuration(120)
            anim.setStartValue(self.offset)
            anim.setEndValue(self._end_offset[self.isChecked()]())
            anim.start()
            self.open_project()


    def enterEvent(self, event):  # pylint: disable=invalid-name
        self.setCursor(Qt.PointingHandCursor)
        super().enterEvent(event)

    def open_project(self):
        pass

    def reset_button(self):
        self.setChecked(False)
        self.offset = self._end_offset[False]()
        # self.app.toggle_server_state(self.title)


