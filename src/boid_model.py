from simulation_settings import SimulationSettings
from vector2d import Vector2D
from colors import *
import pygame
import random
from constants import *
from tri import DrawableTriangle
from triangle import getCenter
import math

class BoidModel():

    def __init__(self, pos=(0,0)) -> None:
        self.settings = SimulationSettings()
        self.pos = Vector2D(pos[0], pos[1])
        self.vel = Vector2D(random.randint(-5, 5), random.randint(-5, 5))
        self.acc = Vector2D()

        # Triangle used to visualize the boid
        self.triangle = DrawableTriangle(10, 60, 0, pos)

    def coherence(self, boids):
        # Coherence, move the boid to the perceived centre of mass of the nearby flock
        nearby_boids = self.get_nearby_boids(boids)
        steer = Vector2D()
        if len(nearby_boids) == 0:
            return Vector2D()

        position_sum = Vector2D()
        for boid in nearby_boids:
            position_sum += boid.pos

        steer = position_sum / len(nearby_boids)

        # Move the boid 1% towards the center
        return (steer - self.pos) / 100

    def separation(self, boids):
        # Separation, make sure that the boid doesn't collide with its nearby flock
        nearby_boids = self.get_nearby_boids(boids)
        steer = Vector2D()

        if len(nearby_boids) == 0:
            return Vector2D()

        for boid in nearby_boids:
            if boid.pos.get_distance(self.pos) < self.settings.get_separation_radius():
                steer -= (boid.pos - self.pos)

        return steer / 16

    def alignment(self, boids):
        # Alignment, Boids try to change their position so it corresponds with the average alignment of its nearby flock
        nearby_boids = self.get_nearby_boids(boids)
        perceived_vel = Vector2D()
        if len(nearby_boids) == 0:
            return Vector2D()

        for boid in nearby_boids:
            perceived_vel += boid.vel

        perceived_vel_avg = perceived_vel / len(nearby_boids)
        return (perceived_vel_avg - self.vel) / 8

    def get_nearby_boids(self, boids):
        # Returns boids within the given boids perception radius
        nearby = []
        for boid in boids:
            if boid is self:
                continue
            distance = self.pos.get_distance(boid.pos)
            if distance <= self.settings.get_boid_perception_radius():
                nearby.append(boid)
        return nearby

    def update(self, boids):
        # Apply rules
        v1 = self.coherence(boids) * self.settings.get_cohesion_factor()
        v2 = self.separation(boids) * self.settings.get_separation_factor()
        v3 = self.alignment(boids) * self.settings.get_alignment_factor()

        self.acc = v1 + v2 + v3
        self.vel += (self.acc)

        self.vel.clamp(1, self.settings.get_max_speed())
        self.pos += self.vel
        """ self.vel -= Vector2D(
            self.vel.x * self.settings.get_boid_drag(),
            self.vel.y * self.settings.get_boid_drag(),
        ) """

        # Handle out of bounds
        if self.settings.get_bounds():
            self.handle_soft_bounds()
        else:
            self.handle_out_of_bounds()
        # Update the triangle component
        self.update_triangle()

    def handle_out_of_bounds(self):
        if self.pos.x > SIM_WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = SIM_WIDTH
        if self.pos.y > WINDOW_HEIGHT:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = WINDOW_HEIGHT

    def handle_soft_bounds(self):
        if self.pos.x < 0:
            self.vel += Vector2D(5, 0)
        elif self.pos.x > SIM_WIDTH:
            self.vel += Vector2D(-5, 0)

        if self.pos.y < 0:
            self.vel += Vector2D(0, 5)
        elif self.pos.y > WINDOW_HEIGHT:
            self.vel += Vector2D(0, -5)

    def update_triangle(self):
        # Updates the position and rotation of the triangle component
        self.triangle.set_pos(self.pos.get_position())
        center = getCenter(self.triangle.tri)
        center_vec = Vector2D(center[0], center[1])
        direction = center_vec.look_at(self.vel+center_vec).get_angle()
        self.triangle.rotate_to_angle(direction, center_vec.x - (self.vel+center_vec).x)

    def draw(self, surface):
        self.triangle.draw(surface, BOID_COLOR, debug=False)

    def get_mouse_vec(self):
        mouse_pos = pygame.mouse.get_pos()
        vec = Vector2D(mouse_pos[0], mouse_pos[1])
        return vec.normalize()
