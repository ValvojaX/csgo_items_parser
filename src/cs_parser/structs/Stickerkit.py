from vdf import VDFDict

from .Base import Base
from .Rarity import Rarity

class Stickerkit(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.rarity: Rarity | None = None

        self.name_tag: str = data.get("item_name")
        self.index: str = data.get("index")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "name_tag": self.name_tag,
            "index": self.index,
            "rarity": None if self.rarity is None else self.rarity.asdict()
        }