"""
    Пакет для css стилей приложения.
Class:
    Styles
"""


class Styles:
    """
     Класс, предоставляющий стили для виджетов и элементов интерфейса.

     Attributes:
         background_medium_dark_grey (str): Цвет фона (medium dark grey).
         transparent_white (str): Прозрачный белый цвет.
         color_white (str): Белый цвет.
         color_black (str): Черный цвет.
         light_medium_dark_grey (str): Светло-серый цвет (medium dark grey).
         light_grey (str): Светло-серый цвет.
         orange_color (str): Оранжевый цвет.
         pixel_0 (str): 0 пикселей.
         pixel_8 (str): 8 пикселей.
         pixel_9 (str): 9 пикселей.
         pixel_10 (str): 10 пикселей.
         pixel_15 (str): 15 пикселей.
         pixel_27 (str): 27 пикселей.
         pixel_44 (str): 44 пикселей.
         shadow_0_4_4 (str): Тень с параметрами (0px 4px 4px rgba(0, 0, 0, 0.40)).
         shadow_0_4_4_0 (str): Тень с параметрами (0px 4px 4px 0px rgba(0, 0, 0, 0.40)).
         font_family_inter (str): Шрифт Inter.
         font_style_normal (str): Нормальный стиль шрифта.
         font_weight_700 (str): Вес шрифта 700.
         line_height_normal (str): Нормальная высота строки.

     Methods:
         to_logo(): Получить стиль для логотипа.
         to_input(): Получить стиль для поля ввода.
         to_connect_btn(): Получить стиль для кнопки подключения.
         to_input_label(): Получить стиль для метки поля ввода.
         to_input_error(): Получить стиль для поля ввода с отображением ошибки.
         to_transparent_widget(): Получить стиль для прозрачного виджета.
         to_body(): Получить стиль для основного контейнера.
         to_bottom(): Получить стиль для нижней части контейнера.
         write_color(): Получить стиль для цвета текста.
         to_version_label(): Получить стиль для метки версии.
     """

    def __init__(self):
        """
            Инициализация класса Styles.

        Все стили разделены на следующие группы:
            -color: цвета
            -pixel: размеры
            -shadow: тени
            -font: Параметры шрифта
        """
        # color
        self.background_medium_dark_grey = "rgba(33, 33, 33, 255)"
        self.transparent_white = "rgba(255,255,255, 0)"
        self.color_white = "white"
        self.color_black = "#000000"
        self.light_medium_dark_grey = "#393939"
        self.light_grey = "#787878"
        self.orange_color = "#f9c747"

        # pixel
        self.pixel_0 = "0px"
        self.pixel_8 = "8px"
        self.pixel_9 = "9px"
        self.pixel_10 = "10px"
        self.pixel_15 = "15px"
        self.pixel_27 = "27px"
        self.pixel_44 = "44px"

        # shadow
        self.shadow_0_4_4 = "0px 4px 4px rgba(0, 0, 0, 0.40)"
        self.shadow_0_4_4_0 = "0px 4px 4px 0px rgba(0, 0, 0, 0.40);"

        # font
        self.font_family_inter = "Inter"
        self.font_style_normal = "normal"
        self.font_weight_700 = "700"
        self.line_height_normal = "normal"


    def to_logo(self) -> str:
        """ Стили для логотипа. """
        return f"""
            background-color: {self.background_medium_dark_grey};
            color: {self.color_white};
            font-size: {self.pixel_44};
            padding-top: {self.pixel_0};
            padding-bottom: {self.pixel_0};
            text-shadow: {self.shadow_0_4_4};
            font-family: {self.font_family_inter};
            font-style: {self.font_style_normal};
            font-weight: {self.font_weight_700};
            line-height: {self.line_height_normal};
            border-top-left-radius: {self.pixel_10};
            border-top-right-radius: {self.pixel_10};
        """

    def to_input(self) -> str:
        """ Стили для поля ввода."""
        return f"""
            border-radius: {self.pixel_8};
            background : {self.color_white};
            height : {self.pixel_27};
            box-shadow : {self.shadow_0_4_4_0};
            padding-left: {self.pixel_10};
        """

    def to_connect_btn(self) -> str:
        """ Стили для кнопки подключения."""
        return f"""
            border-radius: {self.pixel_8};
            background : {self.orange_color};
            height : {self.pixel_27};
            color: {self.color_black};
            box-shadow : {self.shadow_0_4_4_0};
            margin-left: {45};
            margin-right: {45};
        """

    def to_input_label(self) -> str:
        """ Стили для заголовка поля ввода."""
        return f"""
            color: {self.light_grey};
        """

    def to_input_error(self) -> str:
        """ Стили для поля ввода с отображением ошибки."""
        return " ".join(["border: 1px solid red;", self.to_input()])

    def to_transparent_widget(self) -> str:
        """ Стили для прозрачного виджета."""
        return f"background-color: {self.transparent_white};"

    def to_body(self) -> str:
        """ Стили для основной части приложения."""
        return f"background-color: {self.light_medium_dark_grey};"

    def to_bottom(self) -> str:
        """ Стили для нижней части приложения."""
        return f"""
            background-color:{self.background_medium_dark_grey};
            border-bottom-left-radius:{self.pixel_15};
            border-bottom-right-radius:{self.pixel_15};
        """

    def write_color(self) -> str:
        """ Стили для цвета текста."""
        return f"color: {self.color_white};"

    def to_version_label(self) -> str:
        """ Стили для метки версии."""
        return " ".join([f"font-size: {self.pixel_9};", self.write_color()])
