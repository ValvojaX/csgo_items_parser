from vdf import VDFDict

from .Base import Base

class GraffitiTint(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.hex_color: str = data.get("hex_color")
        self.id: str = data.get("id")

        self.name_tag = f"Attrib_SprayTintValue_{self.id}"

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "hex_color": self.hex_color,
            "name_tag": self.name_tag,
            "id": self.id
        }