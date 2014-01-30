import pygame, sys
import random
from pygame.locals import *
from rui.rui import World
from systems import MovementSystem, QuadTreeCollisionSystem, CollisionSystem, RenderSystem
from components import Position, Velocity, Bounds, Color

pygame.init()

WIDTH = 600
HEIGHT = 600
QUADTREE = True

window = pygame.display.set_mode((WIDTH, HEIGHT))
fps_clock = pygame.time.Clock()

pygame.display.set_caption('quadtree')

world = World()

world.add_system(MovementSystem(WIDTH, HEIGHT))
if QUADTREE:
    world.add_system(QuadTreeCollisionSystem(WIDTH, HEIGHT))
else:
    world.add_system(CollisionSystem())

world.add_system(RenderSystem(window))

def create_thing():
    px = random.randint(0, WIDTH)
    py = random.randint(0, HEIGHT)
    vx = random.randint(-5, 5)
    vy = random.randint(-5, 5)
    thing = world.create_entity()
    thing.add_component(Position(px,py))
    thing.add_component(Velocity(vx,vy))
    thing.add_component(Bounds(10,10))
    thing.add_component(Color(pygame.Color(0,0,255)))
    return thing

for _ in range(0, 100):
    world.add_entity(create_thing())

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    world.process()
    pygame.display.update()
    #fps_clock.tick(60)
