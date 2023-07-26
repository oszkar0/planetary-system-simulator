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
        self.orbit = []

    def draw(self, window):
        x = self.x * HeavenlyBody.PLANET_DIST_SCALE + (WIDTH / 2)
        y = self.y * HeavenlyBody.PLANET_DIST_SCALE + (HEIGHT / 2)

        pygame.draw.circle(window, self.color, (x, y), self.radius)

        scaled_orbit_points = []

        if len(self.orbit) >= 2:
            for point in self.orbit:
                x = point[0] * HeavenlyBody.PLANET_DIST_SCALE + (WIDTH / 2)
                y = point[1] * HeavenlyBody.PLANET_DIST_SCALE + (HEIGHT / 2)

                scaled_orbit_points.append((x, y))

            pygame.draw.lines(WINDOW, WHITE, False, scaled_orbit_points)

    def calculate_attraction(self, other_body):
        x_diff = other_body.x - self.x
        y_diff = other_body.y - self.y

        dist_sq = x_diff ** 2 + y_diff ** 2

        force = HeavenlyBody.G * self.mass * other_body.mass / dist_sq

        alfa = math.atan2(y_diff, x_diff)
        force_y = math.sin(alfa) * force
        force_x = math.cos(alfa) * force

        self.total_force_x += force_x
        self.total_force_y += force_y
        other_body.total_force_x -= force_x
        other_body.total_force_y -= force_y

    def calculate_velocity(self):
        self.vel_x += (self.total_force_x / self.mass * HeavenlyBody.TIMESTEP)
        self.vel_y += (self.total_force_y / self.mass * HeavenlyBody.TIMESTEP)

    def update_position(self):
        self.x += (HeavenlyBody.TIMESTEP * self.vel_x)
        self.y += (HeavenlyBody.TIMESTEP * self.vel_y)

        if len(self.orbit) > 100:
            self.orbit.pop(0)

        self.orbit.append((self.x, self.y))


#  method for generating set of pairs object-object
#  such that object must not be in pair with itself
#  and there must only be one pair of object-object
#  regardless of order in pair
def generate_pairs(objects_list):
    pairs = set()
    seen_pairs = set()

    for i in range(len(objects_list)):
        for j in range(i + 1, len(objects_list)):
            pair = (objects_list[i], objects_list[j])

            if pair[0] != pair[1] and pair not in seen_pairs:
                pairs.add(pair)
                seen_pairs.add(pair)

    return pairs


def main():
    run = True
    clock = pygame.time.Clock()

    sun = HeavenlyBody(0, 0, 15, YELLOW, 2e30, 0, 0)
    earth = HeavenlyBody(-HeavenlyBody.AU, 0, 5, BLUE, 6e24, 0, 29783)
    mars = HeavenlyBody(1.5 * HeavenlyBody.AU, 0, 7, RED, 6.39e23, 0, 24130)
    venus = HeavenlyBody(-0.7 * HeavenlyBody.AU, 0, 6, CYAN, 4.87e24, 0, 35000)
    mercury = HeavenlyBody(-0.3 * HeavenlyBody.AU, 0, 3, MAGENTA, 3.3e23, 0, 47000)

    planets = [sun, earth, mars, venus, mercury]

    pairs = generate_pairs(planets)

    while run:
        clock.tick(60)

        WINDOW.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for (planet1, planet2) in pairs:
            planet1.calculate_attraction(planet2)

        for planet in planets:
            planet.draw(WINDOW)
            planet.calculate_velocity()
            planet.update_position()
            planet.total_force_x, planet.total_force_y = 0, 0

        pygame.display.update()

    pygame.quit()


main()
