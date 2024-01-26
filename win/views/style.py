class Styles:
    def __init__(self):
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

        # height

    def to_logo(self):
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

    def to_input(self):
        return f"""
            border-radius: {self.pixel_8};
            background : {self.color_white};
            height : {self.pixel_27};
            box-shadow : {self.shadow_0_4_4_0};

            padding-left: {self.pixel_10};
        """

    def to_connect_btn(self):
        return f"""
            border-radius: {self.pixel_8};
            background : {self.orange_color};
            height : {self.pixel_27};
            color: {self.color_black};
            box-shadow : {self.shadow_0_4_4_0};
            margin-left: {45};
            margin-right: {45};
        """

    def to_input_label(self):
        return f"""
            color: {self.light_grey};
        """

    def to_input_error(self):
        return " ".join(["border: 1px solid red;", self.to_input()])

    def to_transparent_widget(self):
        return f"background-color: {self.transparent_white};"

    def to_body(self):
        return f"background-color: {self.light_medium_dark_grey};"

    def to_bottom(self):
        return f"""
            background-color:{self.background_medium_dark_grey};
            border-bottom-left-radius:{self.pixel_15};
            border-bottom-right-radius:{self.pixel_15};
        """

    def write_color(self):
        return f"color: {self.color_white};"

    def to_version_label(self):
        return " ".join([f"font-size: {self.pixel_9};", self.write_color()])