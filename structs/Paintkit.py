from structs.Base import Base
from structs.Rarity import Rarity

class Paintkit(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.rarity: Rarity = None

        self.name_tag = data.get("description_tag")
        self.wear_default = data.get("wear_default")
        self.wear_remap_min = data.get("wear_remap_min")
        self.wear_remap_max = data.get("wear_remap_max")
        self.index = data.get("index")

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