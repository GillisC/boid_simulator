# Singleton class to store simulation settings
class SimulationSettings:
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super().__new__(cls)
            cls.instance.boid_amount = 100
            cls.instance.boid_perception_radius = 60
            cls.instance.boid_drag = 0.05
            cls.instance.cohesion_factor = 1
            cls.instance.separation_factor = 1
            cls.instance.separation_radius = 20
            cls.instance.alignment_factor = 1
            cls.instance.bounds = True
            cls.instance.min_spped = 1
            cls.instance.max_speed = 10
            cls.instance.random_factor = 0.2
            cls.instance.is_debug = False
        return cls.instance

    # Getters
    def get_boid_amount(self) -> int:
        return self.boid_amount

    def get_boid_perception_radius(self) -> int:
        return self.boid_perception_radius

    def get_boid_drag(self) -> float:
        return self.boid_drag

    def get_cohesion_factor(self) -> float:
        return self.cohesion_factor

    def get_separation_factor(self) -> float:
        return self.separation_factor

    def get_separation_radius(self) -> int:
        return self.separation_radius

    def get_alignment_factor(self) -> float:
        return self.alignment_factor

    def get_bounds(self) -> bool:
        return self.bounds

    def get_min_speed(self) -> float:
        return self.min_speed

    def get_max_speed(self) -> float:
        return self.max_speed

    def get_random_factor(self) -> float:
        return self.random_factor

    def get_debug_state(self) -> bool:
        return self.is_debug

    # Setters
    def set_boid_amount(self, boid_amount: int) -> None:
        self.boid_amount = boid_amount

    def set_boid_perception_radius(self, boid_perception_radius: int) -> None:
        self.boid_perception_radius = boid_perception_radius

    def set_boid_drag(self, boid_drag: float) -> None:
        self.boid_drag = boid_drag

    def set_cohesion_factor(self, cohesion_factor: float) -> None:
        self.cohesion_factor = cohesion_factor

    def set_separation_factor(self, separation_factor: float) -> None:
        self.separation_factor = separation_factor

    def set_separation_radius(self, separation_radius: int) -> None:
        self.separation_radius = separation_radius

    def set_alignment_factor(self, alignment_factor: float) -> None:
        self.alignment_factor = alignment_factor

    def set_bounds(self, bounds: bool) -> None:
        self.bounds = bounds

    def set_max_speed(self, max_speed: float) -> None:
        self.max_speed = max_speed

    def set_min_speed(self, min_speed: float) -> None:
        self.min_speed = min_speed

    def set_random_factor(self, random_factor: float) -> None:
        self.random_factor = random_factor

    def set_debug_state(self, state: bool) -> None:
        self.is_debug = state


if __name__ == "__main__":
    settings1 = SimulationSettings()
    settings2 = SimulationSettings()
    settings1.set_boid_amount(100)
    print(settings2.get_boid_amount())  # 100
    print(settings1 is settings2)  # True
