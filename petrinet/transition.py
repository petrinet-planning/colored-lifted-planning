from .guard import Guard

class Transition:
    name: str
    id: str
    guard: Guard

    def __init__(self, name: str) -> None:
        self.name = name
        self.guard = None

    def add_guard(self, guard: Guard) -> Guard:
        self.guard = guard
        return guard

    def generate_pnml(self, position: tuple[int, int]) -> str:
        guard_pnml = self.guard.generate_pnml() if self.guard else ""
        return f'''\
            <transition id="{self.name}">
                <name><graphics><offset x="0" y="0"/></graphics><text>{self.name}</text></name>
                <graphics><position x="{position[0]}" y="{position[1]}"/></graphics>{guard_pnml}
            </transition>
        '''
