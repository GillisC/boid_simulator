import pygame
from settings import *
from colors import *
import random
import math
from boid_model import BoidModel
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

class BoidSimulator:

    def __init__(self) -> None:
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.sim_surface = pygame.Surface((SIM_WIDTH, WINDOW_HEIGHT))
        self.interface_surface = pygame.Surface((INTERFACE_WIDTH, WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True
        self.boids = []

        self.cohesion_slider = Slider(
            self.interface_surface, 10, 10, 300, 10, min=0, max=25, step=1
        )
        self.cohesion_label = TextBox(self.interface_surface, 10, 30, 20, 10)
        self.cohesion_label.disable()

    def setup(self):
        for _ in range(BOID_AMOUNT):
            boid = BoidModel(
                (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            )
            self.boids.append(boid)

    def handle_events(self, events):
        for event in events:

            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        self.setup()
        while self.running:
            self.clock.tick(FPS)

            self.sim_surface.fill(BACKGROUND)
            self.interface_surface.fill(INTERFACE_BACKGROUND)

            # Handle events
            events = pygame.event.get()
            self.handle_events(events)

            # Update and draw boids
            for boid in self.boids:
                boid.update(self.boids)
                boid.draw(self.sim_surface)

            # print(self.cohesion_slider.getX(), self.cohesion_slider.getY())
            self.cohesion_slider.listen(events)
            self.cohesion_slider.draw()
            self.cohesion_label.setText(self.cohesion_slider.getValue())
            self.cohesion_label.draw()
            # pygame_widgets.update(events)

            # Blit the surfaces onto the main window
            self.window.blit(self.sim_surface, (0, 0))
            self.window.blit(self.interface_surface, (SIM_WIDTH, 0))

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Boid simulator")
    boid_sim = BoidSimulator()
    boid_sim.run()
