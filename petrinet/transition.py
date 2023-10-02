class Transition:
    name: str
    id: str

    def __init__(self, name: str) -> None:
        self.name = name

    def generate_pnml(self, position: tuple[int, int]) -> str:
        return f'''\
            <transition id="{self.name}">
                <name><graphics><offset x="0" y="0"/></graphics><text>{self.name}</text></name>
                <graphics><position x="{position[0]}" y="{position[1]}"/></graphics>
            </transition>
        '''
