import pygame
import math

class Whirlpool:

    RADIUS = 180
    FORCE = 520
    MIN_DIST = 30
    DURATION = 3.0
    FADE_START = 0.6
    MAX_WHIRLPOOLS = 10
    COOLDOWN = 0.4

    OUTER_RADIUS = 68
    INNER_RADIUS = 18
    NUM_ARMS = 3
    ARC_DEGREES = 90
    COLOR_OUTER = (100, 210, 255)
    COLOR_INNER = (200, 240, 255)
    PARTICLE_COUNT = 8

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.age = 0.0
        self.alive = True
        self._spin = 0.0
        self._particles = self._init_particles()

    def _init_particles(self):
        particles = []
        for i in range(self.PARTICLE_COUNT):
            angle = (2 * math.pi / self.PARTICLE_COUNT) * i
            dist = self.OUTER_RADIUS * 0.55
            particles.append({
                "angle": angle,
                "dist": dist,
                "speed": 2.5 + (i % 3) * 0.6,
                "size": 3 + (i % 3),
                "offset": i * 0.4,
            })
        return particles

    def update(self, dt: float):
        self.age += dt
        self._spin += dt * 2.8
        for p in self._particles:
            p["angle"] += dt * p["speed"]
        if self.age >= self.DURATION:
            self.alive = False

    def apply_force(self, player, dt: float):
        dx = self.x - player.x
        dy = self.y - player.y
        dist = math.hypot(dx, dy)

        if dist > self.RADIUS:
            return False

        eff_dist = max(dist, self.MIN_DIST)
        strength = self.FORCE * (self.RADIUS / eff_dist) ** 1.4

        if dist > 0:
            tx = -dy / dist
            ty = dx / dist
        else:
            tx, ty = 1.0, 0.0

        player.vx += tx * strength * dt
        player.vy += ty * strength * dt
        return True

    def draw(self, surface: pygame.Surface, camera_x: float = 0, camera_y: float = 0):
        if not self.alive:
            return

        sx = int(self.x - camera_x)
        sy = int(self.y - camera_y)

        life_frac = self.age / self.DURATION
        alpha = 255 if life_frac < self.FADE_START else int(255 * (1.0 - (life_frac - self.FADE_START) / (1.0 - self.FADE_START)))

        size = (self.OUTER_RADIUS * 2 + 10, self.OUTER_RADIUS * 2 + 10)
        surf = pygame.Surface(size, pygame.SRCALPHA)
        cx = size[0] // 2
        cy = size[1] // 2

        for arm in range(self.NUM_ARMS):
            base_angle = self._spin + arm * (2 * math.pi / self.NUM_ARMS)
            start_rad = base_angle
            end_rad = base_angle + math.radians(self.ARC_DEGREES)
            rect_o = pygame.Rect(cx - self.OUTER_RADIUS, cy - self.OUTER_RADIUS, self.OUTER_RADIUS * 2, self.OUTER_RADIUS * 2)
            pygame.draw.arc(surf, (*self.COLOR_OUTER, alpha), rect_o, start_rad, end_rad, 4)

            offset_rad = start_rad + math.radians(30)
            rect_i = pygame.Rect(cx - self.INNER_RADIUS, cy - self.INNER_RADIUS, self.INNER_RADIUS * 2, self.INNER_RADIUS * 2)
            pygame.draw.arc(surf, (*self.COLOR_INNER, alpha), rect_i, offset_rad, offset_rad + math.radians(self.ARC_DEGREES), 3)

        for p in self._particles:
            px = cx + int(p["dist"] * math.cos(p["angle"]))
            py = cy + int(p["dist"] * math.sin(p["angle"]))
            pygame.draw.circle(surf, (*self.COLOR_OUTER, alpha), (px, py), p["size"])

        pygame.draw.circle(surf, (*self.COLOR_INNER, alpha), (cx, cy), 6)
        surface.blit(surf, (sx - size[0] // 2, sy - size[1] // 2))

class WhirlpoolManager:
    def __init__(self):
        self.whirlpools: list[Whirlpool] = []
        self._cooldown_timer = 0.0

    def handle_event(self, event: pygame.event.Event, camera_x: float = 0, camera_y: float = 0):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._cooldown_timer <= 0 and len(self.whirlpools) < Whirlpool.MAX_WHIRLPOOLS:
                mx, my = event.pos
                wx = mx + camera_x
                wy = my + camera_y
                self.whirlpools.append(Whirlpool(wx, wy))
                self._cooldown_timer = Whirlpool.COOLDOWN

    def update(self, dt: float, player):
        self._cooldown_timer = max(0.0, self._cooldown_timer - dt)
        for wp in self.whirlpools:
            wp.update(dt)
            if wp.alive:
                wp.apply_force(player, dt)
        self.whirlpools = [wp for wp in self.whirlpools if wp.alive]

    def draw(self, surface: pygame.Surface, camera_x: float = 0, camera_y: float = 0):
        for wp in self.whirlpools:
            wp.draw(surface, camera_x, camera_y)

    @property
    def count(self) -> int:
        return len(self.whirlpools)

    def clear(self):
        self.whirlpools.clear()