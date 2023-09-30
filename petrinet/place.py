from petrinet.color import Color

class Place:
    name: str
    id: str

    def __init__(self, name: str, color: Color) -> None:
        self.name = name
        self.color = color
