from structs.Base import Base

class Quality(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.value = data.get("value")
        self.weight = data.get("weight")
        self.hex_color = data.get("hexColor")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "value": self.value,
            "weight": self.weight,
            "hex_color": self.hex_color
        }