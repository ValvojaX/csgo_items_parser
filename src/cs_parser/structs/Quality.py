from vdf import VDFDict

from .Base import Base

class Quality(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.value: str = data.get("value")
        self.weight: str = data.get("weight")
        self.hex_color: str = data.get("hexColor")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "value": self.value,
            "weight": self.weight,
            "hex_color": self.hex_color
        }