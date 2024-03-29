from csgo_items_parser.structs.Base import Base
from csgo_items_parser.structs.Rarity import Rarity

class Stickerkit(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.rarity: Rarity = None

        self.name_tag = data.get("item_name")
        self.index = data.get("index")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "name_tag": self.name_tag,
            "index": self.index,
            "rarity": None if self.rarity is None else self.rarity.asdict()
        }