import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Fireworks 2025")

clock = pygame.time.Clock()
BLACK = (6, 6, 15)

# --- Load explosion sound ---
explosion_sound = pygame.mixer.Sound("sound.mp3.mp3")
explosion_sound.set_volume(0.5)  # adjust volume if needed

def color_cycle(t):
    return (
        int(128 + 127 * math.sin(t)),
        int(128 + 127 * math.sin(t + 2)),
        int(128 + 127 * math.sin(t + 4))
    )

def heart(t, s=6):
    x = s * 16 * math.sin(t)**3
    y = -s * (
        13 * math.cos(t)
        - 5 * math.cos(2*t)
        - 2 * math.cos(3*t)
        - math.cos(4*t)
    )
    return x, y

class Particle:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(90, 130)
        self.size = 2
        self.t = random.uniform(0, 6)

    def update(self):
        self.vy += 0.035
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.t += 0.05

    def draw(self, surf):
        if self.life > 0:
            pygame.draw.circle(
                surf,
                color_cycle(self.t),
                (int(self.x), int(self.y)),
                self.size
            )

class Rocket:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT
        self.launch_type = random.choice(["straight", "left", "right"])

        if self.launch_type == "straight":
            self.vx = 0
            self.vy = random.uniform(-16, -19)
        elif self.launch_type == "left":
            self.vx = random.uniform(-4, -6)
            self.vy = random.uniform(-14, -16)
        else:
            self.vx = random.uniform(4, 6)
            self.vy = random.uniform(-14, -16)

        self.trail = []
        self.exploded = False
        self.particles = []
        self.t = random.uniform(0, 6)

    def explode(self):
        cx, cy = self.x, self.y

        # --- Play explosion sound ---
        explosion_sound.play()

        for i in range(160):
            a = (2 * math.pi / 160) * i
            self.particles.append(
                Particle(cx, cy, a, random.uniform(3.8, 4.8))
            )

        for i in range(120):
            t = (2 * math.pi / 120) * i
            hx, hy = heart(t)
            ang = math.atan2(hy, hx)
            self.particles.append(
                Particle(cx, cy, ang, random.uniform(2.3, 3.2))
            )

        self.exploded = True

    def update(self):
        if not self.exploded:
            self.x += self.vx
            self.y += self.vy
            self.vy += 0.13
            self.t += 0.15

            self.trail.append((self.x, self.y, self.t))
            if len(self.trail) > 22:
                self.trail.pop(0)

            if self.vy >= 0:
                self.explode()
        else:
            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, surf):
        if not self.exploded:
            for i, (tx, ty, tt) in enumerate(self.trail):
                alpha = i * 10
                s = pygame.Surface((6, 6), pygame.SRCALPHA)
                pygame.draw.circle(
                    s,
                    (*color_cycle(tt), alpha),
                    (3, 3),
                    2
                )
                surf.blit(s, (tx - 3, ty - 3))

        for p in self.particles:
            p.draw(surf)

font = pygame.font.SysFont("arialblack", int(WIDTH * 0.1), bold=True)

fireworks = []
running = True
t_text = 0

while running:
    clock.tick(60)
    screen.fill(BLACK)

    t_text += 0.03
    text_color = color_cycle(t_text)
    text_surf = font.render("GOODBYE 2025", True, text_color)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surf, text_rect)

    if random.random() < 0.045:
        fireworks.append(Rocket())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    for fw in fireworks:
        fw.update()
        fw.draw(screen)

    fireworks = [fw for fw in fireworks if not fw.exploded or fw.particles]

    pygame.display.flip()

pygame.quit()
