from vdf import VDFDict
from ..utils import vdf_dict_to_dict_recursive, vdf_copy_inner_values

from .Base import Base
from .Quality import Quality
from .Rarity import Rarity

class Prefab(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.prefabs: [Prefab] = []
        self.quality: Quality | None = None
        self.rarity: Rarity | None = None

        if data is not None:
            attributes = vdf_copy_inner_values(data, "attributes")
            attributes.remove_all_for("attributes")
            self.attributes: dict = vdf_dict_to_dict_recursive(attributes.copy())

        if data is not None:
            tags = vdf_copy_inner_values(data, "tags")
            tags.remove_all_for("tags")
            self.tags: dict = vdf_dict_to_dict_recursive(tags.copy())

        self.name_tag: str = data.get("item_name")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "name_tag": self.name_tag,
            "attributes": self.attributes,
            "tags": self.tags,
            "quality": None if self.quality is None else self.quality.asdict(),
            "rarity": None if self.rarity is None else self.rarity.asdict(),
            "prefabs": [i.asdict() for i in self.prefabs]
        }