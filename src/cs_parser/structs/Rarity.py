from vdf import VDFDict

from .Base import Base

class Rarity(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.value: str = data.get("value")
        self.name_tag: str = data.get("loc_key")
        self.name_tag_weapon: str = data.get("loc_key_weapon")
        self.name_tag_character: str = data.get("loc_key_character")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "value": self.value,
            "name_tag": self.name_tag,
            "name_tag_weapon": self.name_tag_weapon,
            "name_tag_character": self.name_tag_character
        }