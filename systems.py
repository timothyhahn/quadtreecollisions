import pygame
from datetime import datetime
from rui.rui import System
from components import Position, Velocity, Bounds, Color
from quadtree import Rectangle, Quadtree



class MovementSystem(System):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.down = True

    def process(self, delta):
        entities = self.world.get_entities_by_components(Position, Velocity)
        for entity in entities:
            position = entity.get_component(Position)
            velocity = entity.get_component(Velocity)
            if position.x <= 0 or position.x >= self.width:
                if position.x < 0:
                    position.x = 10
                else:
                    position.x = self.width - 10
                velocity.x = -velocity.x

            if position.y <= 0 or position.y >= self.height:
                if position.y < 0:
                    position.y = 10
                else:
                    position.y = self.height - 10
                velocity.y = -velocity.y
            velocity.y += 1
            position.x += velocity.x * delta
            position.y += velocity.y * delta


def value_in_range(value, min, max):
    return value >= min and value <= max

def does_collide(you, obstacle):
    you_position = you.get_component(Position)
    you_bounds = you.get_component(Bounds)
    ob_position = obstacle.get_component(Position)
    ob_bounds = obstacle.get_component(Bounds)

    xOverlap = value_in_range(you_position.x, ob_position.x, ob_position.x + ob_bounds.x)\
            or value_in_range(ob_position.x, you_position.x, you_position.x + you_bounds.x)
    yOverlap = value_in_range(you_position.y, ob_position.y, ob_position.y + ob_bounds.y)\
            or value_in_range(ob_position.y, you_position.y, you_position.y + you_bounds.y)
    return xOverlap and yOverlap


class QuadTreeCollisionSystem(System):
    def __init__(self, width, height):
        self.quad = Quadtree(0, Rectangle(0,0,width, height))
        self.counter = 0
        self.time_passed_total = 0
        
    def process(self, delta):
        start = datetime.now()
        entities = self.world.get_entities_by_components(Position, Bounds)

        self.quad.clear()

        for entity in entities:
            self.quad.insert(entity)

        for entity in entities:
            return_objects = []
            return_objects = self.quad.retrieve(entity)
            for against in return_objects:
                if entity != against:
                    if does_collide(entity, against):
                        entity.get_component(Color).color = pygame.Color(150, 0, 155)
        
        elapsed = datetime.now() - start
        self.counter += 1
        self.time_passed_total += elapsed.microseconds

        if self.counter % 10 == 0:
            print 'collisions take on average %s milliseconds' % (self.time_passed_total / self.counter / 1000)
            for entity in entities:
                entity.get_component(Color).color = pygame.Color(0,0,255)

class ImpQuadTreeCollisionSystem(System):
    def __init__(self, width, height):
        self.quad = Quadtree(0, Rectangle(0,0,width, height))
        self.counter = 0
        self.time_passed_total = 0
        
    def process(self, delta):
        start = datetime.now()
        entities = self.world.get_entities_by_components(Position, Bounds)

        self.quad.clear()

        for entity in entities:
            self.quad.insert2(entity)

        quads = self.quad.retrieve_quadrants()

        counter = 0
        for quad in quads:
            counter += len(quad)
            while len(quad) > 1:
                head, rest = quad[0], quad[1:]
                for against in rest:
                    if does_collide(head, against):
                        head.get_component(Color).color = pygame.Color(150, 0, 0)
                        against.get_component(Color).color = pygame.Color(150, 0, 0)
                quad = rest
        
        elapsed = datetime.now() - start
        self.counter += 1
        self.time_passed_total += elapsed.microseconds

        if self.counter % 50 == 0:
            print 'collisions take on average %s milliseconds' % (self.time_passed_total / self.counter / 1000)
            for entity in entities:
                entity.get_component(Color).color = pygame.Color(0,0,255)



class CollisionSystem(System):
    def __init__(self):
        self.counter = 0
        self.time_passed_total = 0

    def process(self, delta):
        start = datetime.now()
        entities = self.world.get_entities_by_components(Position, Bounds)
        for entity in entities:
            for against in entities:
                if entity is not against:
                    if does_collide(entity, against):
                        entity.get_component(Color).color = pygame.Color(0, 150, 150)
        elapsed = datetime.now() - start
        self.counter += 1
        self.time_passed_total += elapsed.microseconds
        if self.counter % 10 == 0:
            print 'collisions take on average %s milliseconds' % (self.time_passed_total / self.counter / 1000)
            for entity in entities:
                entity.get_component(Color).color = pygame.Color(0,0,255)

class RenderSystem(System):
    def __init__(self, window):
        self.window = window

    def process(self, delta):
        self.window.fill(pygame.Color(255,255,255))
        entities = self.world.get_entities_by_components(Position, Bounds, Color)
        for entity in entities:
            color = entity.get_component(Color).color
            position = entity.get_component(Position)
            bounds = entity.get_component(Bounds)

            rect = pygame.Rect(position.x, position.y, bounds.x, bounds.y)
            pygame.draw.rect(self.window, color, rect)
