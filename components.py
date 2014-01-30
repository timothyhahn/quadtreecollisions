from rui.rui import Component

class Position(Component):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return 'x: %s, y: %s' % (self.x, self.y)


class Velocity(Component):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return 'x: %s, y: %s' % (self.x, self.y)

class Bounds(Component):
    def __init__(self, x = 5, y =  5):
        self.x = x
        self.y = y
    def __str__(self):
        return 'x: %s, y: %s' % (self.x, self.y)

class Color(Component):
    def __init__(self, color):
        self.color = color

