from csgo_items_parser.structs.Base import Base
from csgo_items_parser.structs.Prefab import Prefab
from csgo_items_parser.structs.Attribute import Attribute
from csgo_items_parser.structs.Quality import Quality
from csgo_items_parser.structs.Rarity import Rarity

class Item(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.prefab: Prefab = None
        self.quality: Quality = None
        self.rarity: Rarity = None

        self.attributes: dict = data.get("attributes", {})
        self.tags: dict = data.get("tags", {})
        self.tool: dict = data.get("tool", {})

        self.name_tag = data.get("item_name")
        self.baseitem = data.get("baseitem")
        self.item_type = data.get("item_type")

        self.index = data.get("index")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "name_tag": self.name_tag,
            "baseitem": self.baseitem,
            "item_type": self.item_type,
            "index": self.index,
            "tool": self.tool,
            "tags": self.tags,
            "attributes": self.attributes,
            "prefab": None if self.prefab is None else self.prefab.asdict(),
            "quality": None if self.quality is None else self.quality.asdict(),
            "rarity": None if self.rarity is None else self.rarity.asdict(),
        }