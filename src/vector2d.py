import math
import pygame
import random

class Vector2D:

    def __init__(self, x=0, y=0) -> None:
        self.x: int = x
        self.y: int = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def set_magnitude(self, mag):
        if self.get_magnitude() == 0:
            return
        scalar = mag / self.get_magnitude()
        self.x = self.x * scalar
        self.y = self.y * scalar

    def get_magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        mag = self.get_magnitude()
        if mag == 0:
            return Vector2D()
        return Vector2D(self.x / mag, self.y / mag)

    def get_angle(self):
        if self.x == 0:
            a = math.atan(self.y)
        else:
            a = math.atan(self.y / self.x)
        return math.degrees(a)

    def get_angle_between(self, other):
        dot = self.x * other.x + self.y * other.y
        det = self.x * other.y - self.y * other.x
        angle = math.atan2(det, dot)
        return math.degrees(angle)

    def look_at(self, other):
        # Returns a normalized vector from self to other
        dx = self.x - other.x
        dy = self.y - other.y
        return Vector2D(dx, dy).normalize()   

    def clamp(self, min, max):
        # Clamps the magnitude of the vector to an upper bound
        mag = self.get_magnitude()
        if mag < min:
            self.set_magnitude(min)
        if mag > max:
            self.set_magnitude(max)

    def random():
        # Returns a random normalized vector
        return Vector2D(random.randint(-5, 5), random.randint(-5, 5)).normalize()

    def get_position(self):
        # Returns the vector as a tuple
        # Useful sometimes
        return (self.x, self.y)

    def get_distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __str__(self):
        return f"Vector2D({self.x}, {self.y})"

if __name__ == "__main__":
    v = Vector2D(-1,0)
    print(v.get_angle())
