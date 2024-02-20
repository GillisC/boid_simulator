import math

WINDOW_WIDTH = 1444
WINDOW_HEIGHT = 1024
SURFACE_RATIO = 3 / 4
SIM_WIDTH = math.floor(WINDOW_WIDTH * SURFACE_RATIO)
INTERFACE_WIDTH = WINDOW_WIDTH - SIM_WIDTH

FPS = 60

# Boid settings
BOID_AMOUNT = 100
BOID_PERCEPTION_RADIUS = 100
BOID_DRAG = 0.05
COHESION_FACTOR = 1
SEPARATION_FACTOR = 1
SEPARATION_RANGE = 40
ALIGNMENT_FACTOR = 1

BOUNDS: bool = True
