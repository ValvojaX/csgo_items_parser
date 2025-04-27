from vdf import VDFDict

from .Base import Base

class Color(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.color_name: str = data.get("color_name")
        self.hex_color: str = data.get("hex_color")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "color_name": self.color_name,
            "hex_color": self.hex_color
        }