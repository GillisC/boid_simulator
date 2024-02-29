from types import NoneType
import pygame
import random


class QuadTree:

    def __init__(self, boundrary, capacity) -> None:
        self.boundary = boundrary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
            if self.northeast.insert(point):
                return True
            elif self.southeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True
            elif self.northwest.insert(point):
                return True

    def query(self, circle, found=None):
        # found is a list that will be populated with the points that are found
        if found is None:
            found = []

        # If the circle does not intersect with the boundary, return
        if not self.boundary.intersects(circle):
            return found

        if len(self.points) > 0:
            for p in self.points:
                if circle.contains(p):
                    found.append(p)

        if self.divided:
            # print("checking divided")
            self.northeast.query(circle, found)
            self.southeast.query(circle, found)
            self.southwest.query(circle, found)
            self.northwest.query(circle, found)

        return found

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        nw = Rectangle(x - w / 2, y - h / 2, w / 2, h / 2)
        self.northwest = QuadTree(nw, self.capacity)
        ne = Rectangle(x + w / 2, y - h / 2, w / 2, h / 2)
        self.northeast = QuadTree(ne, self.capacity)
        sw = Rectangle(x - w / 2, y + h / 2, w / 2, h / 2)
        self.southwest = QuadTree(sw, self.capacity)
        se = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)
        self.southeast = QuadTree(se, self.capacity)
        self.divided = True

    def clear(self):
        self.divided = False
        self.points = []
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                self.boundary.x - self.boundary.w,
                self.boundary.y - self.boundary.h,
                self.boundary.w * 2,
                self.boundary.h * 2,
            ),
            1,
        )
        if self.divided:
            self.northeast.draw(screen)
            self.southeast.draw(screen)
            self.southwest.draw(screen)
            self.northwest.draw(screen)


# Rectangle class where x, y is the center of the rectangle
# and w, h are the half width and half height
class Rectangle:

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def contains(self, point):
        return (
            point.x >= self.x - self.w
            and point.x <= self.x + self.w
            and point.y >= self.y - self.h
            and point.y <= self.y + self.h
        )

    def intersects(self, circle):
        # Checks if a circle intersects with the rectangle
        closest_x = clamp(circle.x, self.x - self.w, self.x + self.w)
        closest_y = clamp(circle.y, self.y - self.h, self.y + self.h)

        distance_x = circle.x - closest_x
        distance_y = circle.y - closest_y

        distance = (distance_x**2) + (distance_y**2)
        if distance < (circle.r**2):
            return True
        return False


class Circle:

    def __init__(self, x, y, r) -> None:
        self.x = x
        self.y = y
        self.r = r

    def contains(self, point):
        return (point.x - self.x) ** 2 + (point.y - self.y) ** 2 <= self.r**2


class Point:

    def __init__(self, x, y, data=None) -> None:
        self.x = x
        self.y = y
        self.data = data
        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 2)


def clamp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    running = True
    Rectangle(400, 400, 400, 400)
    quadtree = QuadTree(Rectangle(400, 400, 400, 400), 4)
    points = []
    while running:
        clock.tick(60)
        screen.fill((20, 20, 20))
        quadtree.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    point = Point(x, y)
                    points.append(point)

        for point in points:
            quadtree.insert(point)
            point.draw(screen)
            point.color = (255, 255, 255)

        x, y = pygame.mouse.get_pos()
        circle = Circle(x, y, 100)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 100, 1)
        found = quadtree.query(circle)
        for p in found:
            p.color = (255, 0, 0)
            pygame.draw.circle(screen, (255, 0, 0), (p.x, p.y), 2)

        quadtree.draw(screen)
        pygame.display.update()

    pygame.quit()
