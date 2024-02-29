from quadtree import Circle
from simulation_settings import SimulationSettings
from vector2d import Vector2D
from colors import *
import pygame
import random
from constants import *
from tri import DrawableTriangle
from triangle import getCenter


class BoidModel:

    def __init__(self, pos=(0, 0)) -> None:
        self.settings = SimulationSettings()
        self.pos = Vector2D(pos[0], pos[1])
        self.vel = Vector2D(random.randint(-5, 5), random.randint(-5, 5))
        self.acc = Vector2D()
        self.temp = 0
        self.mouse_down = False

        # Triangle used to visualize the boid
        self.triangle = DrawableTriangle(10, 60, 0, pos)

    def coherence(self, boids):
        # Coherence, move the boid to the perceived centre of mass of the nearby flock
        if len(boids) == 0:
            return Vector2D()

        position_sum = Vector2D()
        for boid in boids:
            position_sum += boid.pos

        steer = position_sum / len(boids)

        # Move the boid 1% towards the center
        return (steer - self.pos) / 100

    def separation(self, boids):
        # Separation, make sure that the boid doesn't collide with its nearby flock
        steer = Vector2D()

        if len(boids) == 0:
            return Vector2D()

        for boid in boids:
            if boid.pos.get_distance(self.pos) < self.settings.get_separation_radius():
                steer -= boid.pos - self.pos

        return steer / 16

    def alignment(self, boids):
        # Alignment, Boids try to change their position so it corresponds with the average alignment of its nearby flock
        perceived_vel = Vector2D()
        if len(boids) == 0:
            return Vector2D()

        for boid in boids:
            perceived_vel += boid.vel

        perceived_vel_avg = perceived_vel / len(boids)
        return (perceived_vel_avg - self.vel) / 8

    def get_nearby_boids(self, quadtree):
        # Returns boids within the given boids perception radius
        nearby = []
        perception = Circle(
            self.pos.x, self.pos.y, self.settings.get_boid_perception_radius()
        )
        boids = quadtree.query(perception)
        for datapoint in boids:
            if datapoint.data is self:
                continue
            nearby.append(datapoint.data)
        return nearby

    def get_nearby_boids_by_radius(self, boids, perception_radius):
        # Returns boids within the given boids perception radius
        nearby = []
        for boid in boids:
            if boid is self:
                continue
            distance = self.pos.get_distance(boid.pos)
            if distance <= perception_radius:
                nearby.append(boid)
        return nearby

    def update(self, quadtree):
        # Apply rules
        nearby = self.get_nearby_boids(quadtree)
        v1 = self.coherence(nearby) * self.settings.get_cohesion_factor()
        v2 = self.separation(nearby) * self.settings.get_separation_factor()
        v3 = self.alignment(nearby) * self.settings.get_alignment_factor()
        v4 = Vector2D.random() * self.settings.get_random_factor()
        v5 = self.move_to_mouse() / 100

        self.acc = v1 + v2 + v3 + v4 + v5
        self.vel += self.acc
        self.temp = self.vel
        self.vel.clamp(1, self.settings.get_max_speed())
        self.pos += self.vel

        # Apply drag
        self.apply_drag()

        # Handle out of bounds
        if self.settings.get_bounds():
            self.handle_soft_bounds()
        else:
            self.handle_out_of_bounds()
        # Update the triangle component
        self.update_triangle()

    def move_to_mouse(self):
        if self.mouse_down:
            mouse_vec = self.get_mouse_vec()
            if (
                mouse_vec.x > 0
                and mouse_vec.x < SIM_WIDTH
                and mouse_vec.y > 0
                and mouse_vec.y < WINDOW_HEIGHT
            ):
                move_vector = mouse_vec - self.pos
                self.mouse_down = False
                return move_vector
            else:
                return Vector2D()
        else:
            return Vector2D()

    def apply_drag(self):
        self.drag = -self.vel
        self.drag.set_magnitude(self.settings.get_boid_drag())
        self.vel += self.drag

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
        direction = center_vec.look_at(self.vel + center_vec).get_angle()
        self.triangle.rotate_to_angle(
            direction, center_vec.x - (self.vel + center_vec).x
        )

    def draw(self, surface):
        color = self.map_vel_to_color()
        self.triangle.draw(surface, color, debug=False)

    def get_mouse_vec(self):
        mouse_pos = pygame.mouse.get_pos()
        vec = Vector2D(mouse_pos[0], mouse_pos[1])
        return vec

    def map_vel_to_color(self):
        norm_x = int((self.vel.normalize().x + 1) * 127.5)
        norm_y = int((self.vel.normalize().y + 1) * 127.5)

        red = norm_x
        green = norm_y
        blue = 0

        red = min(max(red, 0), 255)
        green = min(max(green, 0), 255)
        blue = min(max(blue, 0), 255)

        return (red, green, blue)
