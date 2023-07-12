from csgo_items_parser.structs.Base import Base

class Color(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.color_name = data.get("color_name")
        self.hex_color = data.get("hex_color")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "color_name": self.color_name,
            "hex_color": self.hex_color
        }