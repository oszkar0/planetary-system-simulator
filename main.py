import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet System Simulation")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)


class HeavenlyBody:
    AU = 1.496e11  # astronomical unit
    G = 6.67428e-11  # constant for attraction calculation
    PLANET_DIST_SCALE = 100 / AU
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass, vel_x, vel_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.total_force_x = 0
        self.total_force_y = 0

    def draw(self, window):
        x = self.x * HeavenlyBody.PLANET_DIST_SCALE + (WIDTH / 2)
        y = self.y * HeavenlyBody.PLANET_DIST_SCALE + (HEIGHT / 2)

        pygame.draw.circle(window, self.color, (x, y), self.radius)


def main():
    run = True
    clock = pygame.time.Clock()

    sun = HeavenlyBody(0, 0, 20, YELLOW, 2e30, 0, 0)

    planets = [sun]

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.draw(WINDOW)

        pygame.display.update()

    pygame.quit()


main()
