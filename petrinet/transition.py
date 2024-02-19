from .guardex import GuardExpression

class Transition:
    name: str
    id: str
    guardex: GuardExpression = None

    def __init__(self, name: str) -> None:
        self.name = name

    def generate_pnml(self, position: tuple[int, int]) -> str:
        guard_pnml = self.guardex.generate_pnml() if self.guardex else ""
        return f'''\
            <transition id="{self.name}">
                <name><graphics><offset x="0" y="0"/></graphics><text>{self.name}</text></name>
                <graphics><position x="{position[0]}" y="{position[1]}"/></graphics>{guard_pnml}
            </transition>
        '''
