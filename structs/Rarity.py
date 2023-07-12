from csgo_items_parser.structs.Base import Base

class Rarity(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.value = data.get("value")
        self.name_tag = data.get("loc_key")
        self.name_tag_weapon = data.get("loc_key_weapon")
        self.name_tag_character = data.get("loc_key_character")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "value": self.value,
            "name_tag": self.name_tag,
            "name_tag_weapon": self.name_tag_weapon,
            "name_tag_character": self.name_tag_character
        }