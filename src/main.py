import pygame
from settings import *
from colors import *
import random
from boid_model import BoidModel

class BoidSimulator:

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.boids = []

    def setup(self):
        for _ in range(BOID_AMOUNT):
            boid = BoidModel((random.randint(0, S_WIDTH), random.randint(0, S_HEIGHT)))
            self.boids.append(boid)
    
    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False


    def run(self):
        self.setup()
        while self.running:
            self.screen.fill(BACKGROUND)
            self.clock.tick(FPS)
            self.handle_events()

            for boid in self.boids:
                boid.update(self.boids)
                boid.draw(self.screen)

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Boid simulator")
    boid_sim = BoidSimulator()
    boid_sim.run()