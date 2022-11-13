import ujson

class Base:
    def __init__(self, codename: str):
        self.codename = codename

    def asdict(self) -> dict:
        return {
            "codename": self.codename
        }

    def __eq__(self, other) -> bool:
        return self.codename == other.codename

    def __repr__(self) -> str:
        return ujson.dumps(self.asdict(), indent=4)

    def __str__(self) -> str:
        return self.codename