from vdf import VDFDict
from ..utils import vdf_dict_to_dict_recursive

from .Base import Base
from .Prefab import Prefab
from .Quality import Quality
from .Rarity import Rarity


class Item(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.prefab: Prefab | None = None
        self.quality: Quality | None = None
        self.rarity: Rarity | None = None

        self.attributes: dict = vdf_dict_to_dict_recursive(data.get("attributes", {}).copy())
        self.tags: dict = vdf_dict_to_dict_recursive(data.get("tags", {}).copy())
        self.tool: dict = vdf_dict_to_dict_recursive(data.get("tool", {}).copy())

        self.name_tag: str = data.get("item_name")
        self.baseitem: str = data.get("baseitem")
        self.item_type: str = data.get("item_type")

        self.index: str = data.get("index")

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