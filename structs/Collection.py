from csgo_items_parser.structs.Base import Base
from csgo_items_parser.structs.Item import Item

class Collection(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.name_tag = data.get("name")
        self.crates: list[Item] = []
        self.items = [i for i in data["items"]]

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "name_tag": self.name_tag,
            "items": self.items,
            "crates": [crate.asdict() for crate in self.crates]
        }