from components import Position, Bounds

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return str('x: %s, y: %s, width: %s, height: %s' % (self.x, self.y, self.width, self.height))

class Quadtree:
    def __init__(self, level, bounds):
        self.level = level
        self.bounds = bounds

        self.MAX_OBJECTS = 20
        self.MAX_LEVELS = 8
        self.objects = []
        self.nodes = [None] * 4
    
    def clear(self):
        self.objects[:] = []
        for node in self.nodes:
            if node:
                node.clear()
                node = None

    def count(self):
        count = len(self.objects)
        for node in self.nodes:
            if node:
                count += node.count()
        return count

    def split(self):
        sub_width = self.bounds.width / 2
        sub_height = self.bounds.height / 2
        x = self.bounds.x
        y = self.bounds.y
        self.nodes[0] = Quadtree(self.level + 1, Rectangle(x + sub_width, y, sub_width, sub_height))
        self.nodes[1] = Quadtree(self.level + 1, Rectangle(x, y, sub_width, sub_height))
        self.nodes[2] = Quadtree(self.level + 1, Rectangle(x, y + sub_height, sub_width, sub_height))
        self.nodes[3] = Quadtree(self.level + 1, Rectangle(x + sub_width, y + sub_height, sub_width, sub_height))

    def get_index(self, entity):
        entity_pos = entity.get_component(Position)
        pos_x = entity_pos.y
        pos_y = entity_pos.y
        entity_bounds = entity.get_component(Bounds)
        entity_width = entity_bounds.x
        entity_height = entity_bounds.y

        index = -1
        vertical_midpoint = self.bounds.x + (self.bounds.width / 2)
        horizontal_midpoint = self.bounds.y + (self.bounds.height / 2)
        top_quadrant = pos_y < horizontal_midpoint and pos_y + entity_height < horizontal_midpoint
        bottom_quadrant = pos_y > horizontal_midpoint

        if pos_x < vertical_midpoint and pos_x + entity_width < vertical_midpoint:
            if top_quadrant:
                index = 1
            elif bottom_quadrant:
                index = 2
        elif pos_x > vertical_midpoint:
            if top_quadrant:
                index = 0
            elif bottom_quadrant:
                index = 3

        return index

    def insert(self, entity):
        if self.nodes[0]:
            index = self.get_index(entity)

            if index != - 1:
                self.nodes[index].insert(entity)
                return

        self.objects.append(entity)

        if len(self.objects) + 1 > self.MAX_OBJECTS and self.level < self.MAX_LEVELS:
            if self.nodes[0] == None:
                self.split()

            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i])
                if index != 1:
                    self.nodes[index].insert(self.objects.pop(i))
                else:
                    i += 1

    def insert2(self, entity):
        index = self.get_index(entity)
        if index >= 0:
            if self.nodes[0]:
                self.nodes[index].insert2(entity)
            else:
                if self.level < self.MAX_LEVELS:
                    self.split()
                    self.nodes[index].insert2(entity)
                else:
                    self.objects.append(entity)
        else:
            self.objects.append(entity)

    def retrieve(self, entity):
        return_objects = []
        index = self.get_index(entity)
        if index != -1 and self.nodes[0] != None:
            return_objects = self.nodes[index].retrieve(entity)

        return_objects = return_objects + self.objects
        return return_objects

    def retrieve_quadrants(self):
        return_objects = []
        if len(self.objects) > 0:
            return_objects.append(self.objects)
        for node in self.nodes:
            if node:
                return_objects += node.retrieve_quadrants()

        return return_objects

