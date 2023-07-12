from csgo_items_parser.structs.Base import Base
from csgo_items_parser.structs.Item import Item

class Lootlist(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.containers: list[Item] = []

        self.aliases: set[str] = {codename}
        self.items: list[str] = []

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "aliases": list(self.aliases),
            "items": self.items,
            "containers": [item.asdict() for item in self.containers]
        }