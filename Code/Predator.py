import math
from pathlib import Path
from Player import Player

import pygame

_ASSETS_DIR = Path(__file__).resolve().parent.parent / "Assets"

KIND_FISH = "fish"
KIND_SQUID = "squid"
KIND_CRAB = "crab"

_KIND_FILES = {
    KIND_FISH: "enemy_fish.png",
    KIND_SQUID: "enemy_squid.png",
    KIND_CRAB: "enemy_crab.png",
}

_DEFAULT_SIZE: dict[str, tuple[int, int]] = {
    KIND_FISH: (96, 48),
    KIND_SQUID: (56, 80),
    KIND_CRAB: (72, 50),
}


class Predator:

    def __init__(
        self,
        x: float,
        y: float,
        target: Player,
        kind: str = KIND_FISH,
        size: tuple[int, int] | None = None,
        speed: float = 70.0,
        stunTime: float = 0,
        
    ):
        if kind not in _KIND_FILES:
            raise ValueError(f"Unknown enemy kind {kind!r}; use {list(_KIND_FILES)}")

        self.x = float(x)
        self.y = float(y)
        self.target = target
        self.kind = kind
        self.stunTime = stunTime
        self.alive = True
        w, h = size if size is not None else _DEFAULT_SIZE[kind]
        self.width, self.height = w, h
        self.speed = speed

        path = _ASSETS_DIR / _KIND_FILES[kind]
        self.image = pygame.image.load(str(path)).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (w, h))

        self.vx = 0.0
        self.vy = 0.0

    def update(self, dt: float):

        if self.stunTime > 0:
            self.stunTime -= dt
            return

        target_x, target_y = self.target.getPosition()

        
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist < 1e-6:
            return
        self.vx = (dx / dist) * self.speed
        self.vy = (dy / dist) * self.speed
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface: pygame.Surface, camera_x: float, camera_y: float):
        surface.blit(self.image, (self.x - camera_x, self.y - camera_y))


    def stun(self):
        self.stunTime = 2.0
        self.vx = 0
        self.vy = 0

