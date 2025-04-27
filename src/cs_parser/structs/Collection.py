from vdf import VDFDict

from .Base import Base
from .Item import Item

class Collection(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.name_tag: str = data.get("name")
        self.crates: list[Item] = []
        self.items: list[str] = [i for i in data["items"]]

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "name_tag": self.name_tag,
            "items": self.items,
            "crates": [crate.asdict() for crate in self.crates]
        }