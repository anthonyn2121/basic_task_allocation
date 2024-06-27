class Node:
    def run(self):
        raise NotImplementedError()

class Selector(Node):
    def __init__(self, children):
        self.children = children

    def run(self):
        for child in self.children:
            if child.run():
                return True
        return False

class Sequence(Node):
    def __init__(self, children):
        self.children = children

    def run(self):
        for child in self.children:
            if not child.run():
                return False
        return True

class Action(Node):
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def run(self):
        return self.func()
