class TypeNode:
    def __init__(self, name, ancestor=None):
        self.name = str(name)
        self.ancestor = ancestor
        self.descendants = []
        self.objects = []