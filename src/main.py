import pygame
from constants import *
from colors import *
import random
import math
from boid_model import BoidModel
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle
import concurrent.futures
import threading
from simulation_settings import SimulationSettings
from vector2d import Vector2D
from quadtree import Point, QuadTree, Rectangle

class BoidSimulator:

    def __init__(self) -> None:
        self.settings = SimulationSettings()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.sim_surface = pygame.Surface((SIM_WIDTH, WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True
        self.boids = []

        self.components_dict = {}

        self.previous_boid_count = self.settings.get_boid_amount()

    def setup(self):
        # Generate boids
        for _ in range(self.settings.get_boid_amount()):
            boid = BoidModel(
                (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            )
            self.boids.append(boid)

        print("Setting up components...")
        self.create_components()

    def handle_events(self, events):
        for event in events:

            if event.type == pygame.QUIT:
                self.running = False

            if pygame.mouse.get_pressed()[0]:
                mouse = BoidModel(pygame.mouse.get_pos())
                nearby_boids = mouse.get_nearby_boids_by_radius(self.boids, 200)
                pygame.draw.circle(
                    self.sim_surface,
                    (255, 255, 255),
                    mouse.pos.get_position(),
                    200,
                    1,
                )
                for boid in nearby_boids:
                    boid.mouse_down = True

    def run(self):
        self.setup()
        quadtree = QuadTree(
            Rectangle(SIM_WIDTH / 2, WINDOW_HEIGHT / 2, SIM_WIDTH, WINDOW_HEIGHT), 4
        )
        while self.running:
            self.clock.tick(FPS)

            self.sim_surface.fill(BACKGROUND)
            self.window.fill(INTERFACE_BACKGROUND)

            quadtree.clear()

            # Handle events
            events = pygame.event.get()

            # Handle boid count change
            self.handle_boid_change()

            # Handle input
            self.handle_events(events)

            # Update quadtree
            for boid in self.boids:
                quadtree.insert(Point(boid.pos.x, boid.pos.y, boid))

            if self.settings.get_debug_state():
                quadtree.draw(self.sim_surface)

            # Update and draw boids
            for boid in self.boids:
                boid.update(quadtree)
                boid.draw(self.sim_surface)

            self.update_sliders()
            pygame_widgets.update(events)

            # Blit the surfaces onto the main window
            self.window.blit(self.sim_surface, (0, 0))

            pygame.display.update()

        pygame.quit()

    def handle_boid_change(self):
        if self.previous_boid_count != self.settings.get_boid_amount():
            diff = self.settings.get_boid_amount() - self.previous_boid_count
            if diff > 0:
                # Add boids
                for _ in range(diff):
                    boid = BoidModel(
                        (
                            random.randint(0, WINDOW_WIDTH),
                            random.randint(0, WINDOW_HEIGHT),
                        )
                    )
                    self.boids.append(boid)
            elif diff < 0:
                # Remove boids
                for _ in range(abs(diff)):
                    if self.boids:
                        self.boids.pop()
            self.previous_boid_count = self.settings.get_boid_amount()

    def update_sliders(self):
        # Update the settings based on the slider values
        for component in self.components_dict:

            if component.__class__ == Slider:
                slider = component
                textbox = self.components_dict.get(slider)[0]  # Get the textbox
                setter = self.components_dict.get(slider)[1]  # Get the setter function
                slider_value = slider.getValue()

                if setter is not None:
                    setter(slider_value)
                prefix_text = textbox.getText().split(":")[0]
                textbox.setText(f"{prefix_text}: {round(slider_value, 1)}")

            elif component.__class__ == Toggle:
                checkbox = component
                textbox = self.components_dict.get(checkbox)[0]
                setter = self.components_dict.get(checkbox)[1]
                if setter is not None:
                    setter(checkbox.getValue())
                prefix_text = textbox.getText().split(":")[0]
                textbox.setText(f"{prefix_text}: {checkbox.getValue()}")

    def create_component(
        self, surface, component, name: str, start=1, min=0, max=50, step=1, setter=None
    ):
        # Creates a slider and a textbox and stores them in a dictionary
        # Setter refers to the setter function in which the component value should be passed
        y_pos = len(self.components_dict.keys()) * 55 + 10
        if component == "slider":
            print("its a slider")
            slider_label = TextBox(
                surface,
                SIM_WIDTH + 10,
                y_pos,
                INTERFACE_WIDTH - 20,
                30,
            )
            slider_label.setText(name)
            slider_label.disable()

            slider = Slider(
                self.window,
                SIM_WIDTH + 10,
                y_pos + 35,
                INTERFACE_WIDTH - 20,
                10,
                initial=start,
                min=min,
                max=max,
                step=step,
            )

            self.components_dict[slider] = [slider_label, setter]

        elif component == "checkbox":
            slider_label = TextBox(
                surface,
                SIM_WIDTH + 10,
                y_pos,
                INTERFACE_WIDTH - 70,
                30,
            )
            slider_label.setText(name)
            slider_label.disable()

            checkbox = Toggle(
                self.window, WINDOW_WIDTH - 50, y_pos + 7, 30, 15, startOn=True
            )

            self.components_dict[checkbox] = [slider_label, setter]

    def create_components(self):

        self.create_component(
            self.window,
            "slider",
            "Boid count:",
            start=self.settings.get_boid_amount(),
            min=0,
            max=1000,
            step=1,
            setter=self.settings.set_boid_amount,
        )
        self.create_component(
            self.window,
            "slider",
            "Cohesion factor:",
            start=self.settings.get_cohesion_factor(),
            min=0,
            max=10,
            step=0.2,
            setter=self.settings.set_cohesion_factor,
        )

        self.create_component(
            self.window,
            "slider",
            "Separation factor:",
            start=self.settings.get_separation_factor(),
            min=0,
            max=10,
            step=0.2,
            setter=self.settings.set_separation_factor,
        )

        self.create_component(
            self.window,
            "slider",
            "Alignment factor:",
            start=self.settings.get_alignment_factor(),
            min=0,
            max=10,
            step=0.2,
            setter=self.settings.set_alignment_factor,
        )

        self.create_component(
            self.window,
            "slider",
            "Separation radius:",
            start=self.settings.get_separation_radius(),
            min=0,
            max=200,
            step=5,
            setter=self.settings.set_separation_radius,
        )

        self.create_component(
            self.window,
            "slider",
            "Perception radius:",
            start=self.settings.get_boid_perception_radius(),
            min=0,
            max=200,
            step=5,
            setter=self.settings.set_boid_perception_radius,
        )

        self.create_component(
            self.window,
            "slider",
            "Max speed:",
            start=self.settings.get_max_speed(),
            min=1,
            max=10,
            step=0.5,
            setter=self.settings.set_max_speed,
        )

        self.create_component(
            self.window,
            "slider",
            "Boid drag:",
            start=self.settings.get_boid_drag(),
            min=0,
            max=5,
            step=0.1,
            setter=self.settings.set_boid_drag,
        )

        self.create_component(
            self.window,
            "checkbox",
            "Bounds active:",
            start=self.settings.get_bounds(),
            min=0,
            max=1,
            step=1,
            setter=self.settings.set_bounds,
        )

        self.create_component(
            self.window,
            "checkbox",
            "Debug:",
            start=self.settings.get_debug_state(),
            min=0,
            max=1,
            step=1,
            setter=self.settings.set_debug_state,
        )
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Boid simulator")
    boid_sim = BoidSimulator()
    boid_sim.run()
