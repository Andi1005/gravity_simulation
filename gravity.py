import math
import time
import random

import pygame

from vector import Vector2


random.seed()
pygame.init()


GRAVITY = 6.6739 * 10**-11
WIDTH = 1900
HEIGHT = 1000


class Simulation:
    def __init__(self):
        self.current_time = time.time()

        # Objects
        self.body_count = 60
        self.bodies = [GravityBody() for _ in range(self.body_count)]

        # Settings
        self.enable_body_traces = False
        self.enable_courser_gravity = False
        self.speed = 1000

    def step(self):
        body_list = self.bodies.copy()
        for body_a in self.bodies:
            body_list.remove(body_a)

            for body_b in body_list:
                distance = Vector2.distance(body_a.position, body_b.position)
                if distance <= body_a.radius + body_b.radius:
                    self.merge_bodies(body_a, body_b)
                    self.bodies.remove(body_b)
                    body_list.remove(body_b)
                    continue

                self.calculate_gravity(body_a, body_b)

        delta_time = self.get_delta_time()
        for body in self.bodies:
            body.update(delta_time)

    def merge_bodies(self, body_a, body_b):
        mass = body_a.mass + body_b.mass
        momentum = body_a.velocity * body_a.mass + body_b.velocity * body_b.mass
        velocity = momentum / mass

        body_a.position = (body_a.position * body_a.mass + body_b.position * body_b.mass) / mass

        body_a.radius = math.sqrt(body_a.radius**2 + body_b.radius**2)
        body_a.mass = mass
        body_a.momentum = momentum
        body_a.velocity = velocity

    def calculate_gravity(self, body_a, body_b):

        diff = body_b.position - body_a.position
        distance = diff.length()

        direction = diff.normalize()

        power = GRAVITY * body_a.mass * body_b.mass / distance**2
        body_a.force += direction * power
        body_b.force += direction * -power

    def get_delta_time(self):
        next_time = time.time()
        dt = time.time() - self.current_time
        self.current_time = next_time
        return dt * self.speed

class GravityBody:

    density = 500_000

    def __init__(self, **kwargs):
        self.radius = kwargs.setdefault("radius", random.uniform(1, 7))

        rand_position = Vector2(
            random.randrange(0, int(WIDTH-self.radius)),
            random.randrange(0, int(HEIGHT-self.radius)))
        self.position = kwargs.setdefault("position", rand_position)

        self.velocity = kwargs.setdefault(
            "velocity",
            Vector2(random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01)))

        self.mass = math.pi * self.radius**2 * self.density
        self.force = 0

        self.color = (255, 255, 255)

    def update(self, delta_time):
        acceleration = self.force / self.mass
        self.velocity += acceleration * delta_time
        self.position += self.velocity * delta_time
        self.force = 0

class Window:
    def __init__(self, caption):
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.background_c = (0, 0, 0)

    def update(self, bodies):
        self.screen.fill(self.background_c)
        for body in bodies:
            self.draw(body)
        pygame.display.update()


    def draw(self, body):
        pygame.draw.circle(
            self.screen,
            body.color,
            body.position.to_float(),
            body.radius)

    def is_running(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True


if __name__ == "__main__":
    env = Simulation()
    win = Window("Gravity")
    while win.is_running():
        env.step()
        win.update(env.bodies)
