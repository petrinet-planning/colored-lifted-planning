from .color import Color


class Place:
    name: str
    id: str

    def __init__(self, name: str, color: Color) -> None:
        self.name = name
        self.color = color

    def generate_pnml(self, marking: "Marking", position: tuple[int, int]) -> str:
        return f'''\
        <place id="{self.name}">
                <name><text>{self.name}</text><graphics><offset x="0" y="0"/></graphics></name>
                <graphics><position x="{position[0]}" y="{position[1]}"/></graphics>
                <type><text>{self.color.name}</text><structure><usersort declaration="{self.color.name}"/></structure></type>
                {marking.generate_pnml(self)}
            </place>
        '''
