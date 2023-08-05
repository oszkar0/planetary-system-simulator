import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 1000
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
ORANGE = (255, 127, 80)

FONT = pygame.font.SysFont("comicsans", 16)


class HeavenlyBody:
    AU = 1.496e11  # astronomical unit
    G = 6.67428e-11  # constant for attraction calculation
    PLANET_DIST_SCALE = 100 / AU
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, planet_name, x, y, radius, color, mass, vel_x, vel_y):
        self.planet_name = planet_name
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

        planet_name_text = FONT.render(f"{self.planet_name}", 1, WHITE)
        WINDOW.blit(
            planet_name_text, (x - planet_name_text.get_width() / 2, y - planet_name_text.get_height() - self.radius)
        )

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

    sun = HeavenlyBody("SUN", 0, 0, 15, YELLOW, 2e30, 0, 0)
    earth = HeavenlyBody("EARTH", -HeavenlyBody.AU, 0, 5, BLUE, 6e24, 0, 29783)
    mars = HeavenlyBody("MARS", -1.5 * HeavenlyBody.AU, 0, 7, RED, 6.39e23, 0, 24130)
    venus = HeavenlyBody("VENUS", -0.7 * HeavenlyBody.AU, 0, 6, CYAN, 4.87e24, 0, 35000)
    mercury = HeavenlyBody("MERCURY", -0.3 * HeavenlyBody.AU, 0, 3, MAGENTA, 3.3e23, 0, 47000)
    jupiter = HeavenlyBody("JUPITER", -4.0 * HeavenlyBody.AU, 0, 10, ORANGE, 1.9e27, 0, 15000)

    planets = [sun, earth, mars, venus, mercury, jupiter]

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
