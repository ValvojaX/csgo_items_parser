from csgo_items_parser.structs.Base import Base
from csgo_items_parser.structs.Quality import Quality
from csgo_items_parser.structs.Rarity import Rarity

class Prefab(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.prefab: Prefab = None
        self.quality: Quality = None
        self.rarity: Rarity = None

        self.attributes: dict = data.get("attributes", {})
        self.tags: dict = data.get("tags", {})

        self.name_tag = data.get("item_name")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "name_tag": self.name_tag,
            "attributes": self.attributes,
            "tags": self.tags,
            "quality": None if self.quality is None else self.quality.asdict(),
            "rarity": None if self.rarity is None else self.rarity.asdict(),
            "prefab": None if self.prefab is None else self.prefab.asdict()
        }