# Define the basic BT nodes
class Node:
    def run(self, agent):
        raise NotImplementedError()

class Selector(Node):
    def __init__(self, children):
        self.children = children

    def run(self, agent):
        for child in self.children:
            if child.run(agent):
                return True
        return False

class Sequence(Node):
    def __init__(self, children):
        self.children = children

    def run(self, agent):
        for child in self.children:
            if not child.run(agent):
                return False
        return True

class Action(Node):
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def run(self, agent):
        return self.func(agent)
