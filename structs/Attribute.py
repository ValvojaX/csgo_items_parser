from csgo_items_parser.structs.Base import Base

class Attribute(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.attribute_type = data.get("attribute_type")
        self.attribute_class = data.get("attribute_class")
        self.hidden = data.get("hidden")
        self.value = data.get("value")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "attribute_class": self.attribute_class,
            "hidden": self.hidden,
            "value": self.value,
        }