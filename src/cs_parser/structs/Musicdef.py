from vdf import VDFDict

from .Base import Base

class Musicdef(Base):
    def __init__(self, codename: str, data: VDFDict):
        super().__init__(codename)
        self.name_tag: str = data.get("loc_name")
        self.index: str = data.get("index")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "name_tag": self.name_tag,
            "index": self.index
        }