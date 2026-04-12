import math
from random import uniform
import pygame as pg
import config as C
from sprites import Asteroid, Ship, UFO
from utils import Vec, rand_edge_pos, rand_unit_vec

class World:
    def __init__(self, sfx_ship=None, sfx_ufo=None, sfx_stone_big=None, sfx_stone_small=None):
        self._sfx_ship = sfx_ship
        self._sfx_ufo = sfx_ufo
        self._sfx_stone_big = sfx_stone_big
        self._sfx_stone_small = sfx_stone_small
        
        # 1. CRIAR GRUPOS PRIMEIRO
        self.bullets = pg.sprite.Group()
        self.ufo_bullets = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.ufos = pg.sprite.Group()
        
        # 2. CRIAR NAVE PASSANDO O GRUPO DE BALAS
        self.ship = Ship(Vec(C.WIDTH / 2, C.HEIGHT / 2), self.bullets)
        
        # 3. CRIAR GRUPO GERAL COM A NAVE DENTRO
        self.all_sprites = pg.sprite.Group(self.ship)
        
        # 4. RESTANTE DAS VARIÁVEIS
        self.score = 0
        self.lives = C.START_LIVES
        self.wave = 0
        self.wave_cool = C.WAVE_DELAY
        self.safe = C.SAFE_SPAWN_TIME
        self.ufo_timer = C.UFO_SPAWN_EVERY
        self.slow_mult = C.SHIP_SLOW_MULT
        self.game_over = False

    def start_wave(self):
        self.wave += 1
        count = 3 + self.wave
        for _ in range(count):
            pos = rand_edge_pos()
            while (pos - self.ship.pos).length() < 150:
                pos = rand_edge_pos()
            ang = uniform(0, math.tau)
            speed = uniform(C.AST_VEL_MIN, C.AST_VEL_MAX)
            vel = Vec(math.cos(ang), math.sin(ang)) * speed
            self.spawn_asteroid(pos, vel, "L")

    def spawn_asteroid(self, pos: Vec, vel: Vec, size: str):
        a = Asteroid(pos, vel, size)
        self.asteroids.add(a)
        self.all_sprites.add(a)

    def spawn_ufo(self):
        if self.ufos: return
        small = uniform(0, 1) < 0.5
        y, x = uniform(0, C.HEIGHT), (0 if uniform(0, 1) < 0.5 else C.WIDTH)
        ufo = UFO(Vec(x, y), small)
        ufo.dir.xy = (1, 0) if x == 0 else (-1, 0)
        self.ufos.add(ufo)
        self.all_sprites.add(ufo)

    def ufo_try_fire(self):
        for ufo in self.ufos:
            bullet = ufo.fire_at(self.ship.pos)
            if bullet:
                self.ufo_bullets.add(bullet)
                self.all_sprites.add(bullet)
                if self._sfx_ufo: self._sfx_ufo.play()

    def try_fire(self):
        # Esta função pode ser mantida para cliques manuais se desejar
        if len(self.bullets) >= C.MAX_BULLETS: return
        b = self.ship.fire()
        if b:
            self.bullets.add(b)
            self.all_sprites.add(b)
            if self._sfx_ship: self._sfx_ship.play()

    def try_dash(self):
        self.ship.try_dash()

    def hyperspace(self):
        self.ship.hyperspace()
        self.score = max(0, self.score - C.HYPERSPACE_COST)

    def update(self, dt: float, keys):
        if keys[pg.K_LALT] and self.ship.energy > 0:
            self.slow_mult = C.SHIP_SLOW_MULT
            self.ship.energy = max(0, self.ship.energy - C.SHIP_SLOW_ENERGY_COST * dt)
        else:
            self.slow_mult = 1
        dt_scaled = self.slow_mult * dt
        self.ship.control(keys, dt)
        self.all_sprites.update(dt_scaled)
        self.ship.update(dt)
        if self.safe > 0:
            self.safe -= dt
            self.ship.invuln = 0.5
        if self.ufos: self.ufo_try_fire()
        else: self.ufo_timer -= dt
        if not self.ufos and self.ufo_timer <= 0:
            self.spawn_ufo()
            self.ufo_timer = C.UFO_SPAWN_EVERY

        self.handle_collisions()

        if not self.asteroids:
            if self.wave_cool <= 0:
                self.start_wave()
                self.wave_cool = C.WAVE_DELAY
            else: self.wave_cool -= dt

    def handle_collisions(self):
        # Jogador vs Asteroides
        hits = pg.sprite.groupcollide(
            self.asteroids, self.bullets, False, True,
            collided=lambda a, b: (a.pos - b.pos).length() < (a.r + b.r)
        )
        for ast in hits:
            self.split_asteroid(ast)
            ast.kill() # Garante que o atingido suma
            self.ship.energy = min(self.ship.max_energy, self.ship.energy + 5)

        # UFO vs Asteroides
        ufo_hits = pg.sprite.groupcollide(
            self.asteroids, self.ufo_bullets, False, True,
            collided=lambda a, b: (a.pos - b.pos).length() < a.r
        )
        for ast in ufo_hits:
            self.split_asteroid(ast)
            ast.kill()

        # Check morte da nave
        if self.ship.invuln <= 0 and self.safe <= 0:
            # Colisão com Asteroides/UFOs/Balas inimigas
            for ast in self.asteroids:
                if (ast.pos - self.ship.pos).length() < (ast.r + self.ship.r):
                    self.ship_die(); break
            for ufo in self.ufos:
                if (ufo.pos - self.ship.pos).length() < (ufo.r + self.ship.r):
                    self.ship_die(); break
            for b in self.ufo_bullets:
                if (b.pos - self.ship.pos).length() < (b.r + self.ship.r):
                    b.kill(); self.ship_die(); break

        # Balas do Jogador vs UFOs
        for ufo in list(self.ufos):
            for b in list(self.bullets):
                if (ufo.pos - b.pos).length() < (ufo.r + b.r):
                    self.score += (C.UFO_SMALL["score"] if ufo.small else C.UFO_BIG["score"])
                    ufo.kill(); b.kill()

    def split_asteroid(self, ast: Asteroid):
        if ast.size in ("L", "M"):
            if self._sfx_stone_big: self._sfx_stone_big.play()
        else:
            if self._sfx_stone_small: self._sfx_stone_small.play()
        self.score += C.AST_SIZES[ast.size]["score"]
        split = C.AST_SIZES[ast.size]["split"]
        pos = Vec(ast.pos)
        for s in split:
            dirv = rand_unit_vec()
            speed = uniform(C.AST_VEL_MIN, C.AST_VEL_MAX) * 1.2
            self.spawn_asteroid(pos, dirv * speed, s)

    def ship_die(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            return
        self.ship.pos.xy = (C.WIDTH / 2, C.HEIGHT / 2)
        self.ship.vel.xy = (0, 0)
        self.ship.angle = -90
        self.ship.dash_cool = 0.0
        self.ship.invuln = C.SAFE_SPAWN_TIME
        self.safe = C.SAFE_SPAWN_TIME

    def draw(self, surf: pg.Surface, font: pg.font.Font):
        for spr in self.all_sprites:
            spr.draw(surf)
        pg.draw.line(surf, (60, 60, 60), (0, 50), (C.WIDTH, 50), width=1)
        txt = f"SCORE {self.score:06d}   LIVES {self.lives}   WAVE {self.wave}"
        label = font.render(txt, True, C.WHITE)
        surf.blit(label, (10, 10))