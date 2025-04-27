from vdf import VDFDict

from .Base import Base
from .Rarity import Rarity

class Paintkit(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.rarity: Rarity | None = None

        self.name_tag: str = data.get("description_tag")
        self.wear_default: str = data.get("wear_default")
        self.wear_remap_min: str = data.get("wear_remap_min")
        self.wear_remap_max: str = data.get("wear_remap_max")
        self.index: str = data.get("index")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "name_tag": self.name_tag,
            "wear_default": self.wear_default,
            "wear_remap_min": self.wear_remap_min,
            "wear_remap_max": self.wear_remap_max,
            "index": self.index,
            "rarity": None if self.rarity is None else self.rarity.asdict()
        }