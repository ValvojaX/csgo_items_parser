from structs.Base import Base

class Musicdef(Base):
    def __init__(self, codename: str, data: dict):
        super().__init__(codename)
        self.name_tag = data.get("loc_name")
        self.index = data.get("index")

    def asdict(self) -> dict:
        return {
            "codename": self.codename,
            "name_tag": self.name_tag,
            "index": self.index
        }