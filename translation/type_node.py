class TypeNode:
    def __init__(self, name, ancestor=None):
        self.name = str(name)
        self.ancestor = ancestor
        self.descendants = []
        self.objects = []
        self.first_object = (str(name).split()[0] + "_s")
        self.last_object = (str(name).split()[0] + "_e")