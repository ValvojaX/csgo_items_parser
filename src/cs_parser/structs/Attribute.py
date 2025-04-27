from vdf import VDFDict

from .Base import Base

class Attribute(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.attribute_type: str | None = data.get("attribute_type")
        self.attribute_class: str  = data.get("attribute_class")
        self.hidden: str = data.get("hidden")
        self.value: str | None = data.get("value")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "attribute_class": self.attribute_class,
            "hidden": self.hidden,
            "value": self.value,
        }