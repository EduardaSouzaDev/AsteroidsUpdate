
# ASTEROIDE SINGLEPLAYER v1.0
# This file manages the application loop, scenes, input handling, and screen drawing.

import random
import sys
from dataclasses import dataclass

import pygame as pg

import config as C
from systems import World
from utils import text


@dataclass
class Scene:
    name: str


class Game:
    # Initialize pygame, shared UI resources, and the initial scene state.
    def __init__(self):
        pg.init()
        if C.RANDOM_SEED is not None:
            random.seed(C.RANDOM_SEED)
        self.logical = pg.Surface((C.WIDTH, C.HEIGHT))
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        pg.display.set_caption("Asteroides")
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("consolas", 20)
        self.big = pg.font.SysFont("consolas", 48)
        self.scene = Scene("menu")
        self.world = World()
        self.final_score = 0    # Pontuação capturada no momento do game over
        self.go_fade = 0.0      # Temporizador de fade-in da tela de game over

    def run(self):
        # Process events, update the active scene, and render each frame.
        while True:
            dt = self.clock.tick(C.FPS) / 1000.0
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
                if e.type == pg.KEYDOWN:
                    # ESC: encerra o jogo nas cenas menu/play; volta ao menu no game over
                    if e.key == pg.K_ESCAPE:
                        if self.scene.name == "game_over":
                            self.scene = Scene("menu")
                        else:
                            pg.quit()
                            sys.exit(0)
                    elif self.scene.name == "play":
                        if e.key == pg.K_SPACE:
                            self.world.try_fire()
                        if e.key == pg.K_LSHIFT:
                            self.world.hyperspace()
                    elif self.scene.name == "menu":
                        self.world = World()
                        self.scene = Scene("play")
                    elif self.scene.name == "game_over":
                        if e.key in (pg.K_RETURN, pg.K_SPACE):
                            self.world = World()
                            self.go_fade = 0.0
                            self.scene = Scene("play")

            keys = pg.key.get_pressed()
            self.logical.fill(C.BLACK)

            if self.scene.name == "menu":
                self.draw_menu()
            elif self.scene.name == "play":
                self.world.update(dt, keys)
                self.world.draw(self.logical, self.font)
                # Verifica se o mundo sinalizou fim de jogo
                if self.world.game_over:
                    self.final_score = self.world.score
                    self.go_fade = 0.0
                    self.scene = Scene("game_over")
            elif self.scene.name == "game_over":
                self.go_fade += dt
                self.draw_game_over()

            self._present()
            pg.display.flip()

    def _present(self):
        sw, sh = self.screen.get_size()
        lw, lh = C.WIDTH, C.HEIGHT
        scale = min(sw / lw, sh / lh)
        nw, nh = max(1, int(lw * scale)), max(1, int(lh * scale))
        scaled = pg.transform.smoothscale(self.logical, (nw, nh))
        self.screen.fill(C.BLACK)
        self.screen.blit(scaled, ((sw - nw) // 2, (sh - nh) // 2))

    def draw_game_over(self):
        # Exibe a tela de game over com fade-in, pontuação final e instruções.
        alpha = min(255, int(255 * self.go_fade / C.GAME_OVER_FADE_DURATION))

        overlay = pg.Surface((C.WIDTH, C.HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        self.logical.blit(overlay, (0, 0))

        if alpha < 60:
            return

        text(self.logical, self.big, "GAME OVER",
             C.WIDTH // 2 - 130, C.HEIGHT // 2 - 100)
        text(self.logical, self.font,
             f"Pontuacao final: {self.final_score:06d}",
             C.WIDTH // 2 - 110, C.HEIGHT // 2 - 20)
        text(self.logical, self.font,
             "Enter / Espaco: jogar novamente",
             C.WIDTH // 2 - 150, C.HEIGHT // 2 + 40)
        text(self.logical, self.font,
             "ESC: menu principal",
             C.WIDTH // 2 - 90, C.HEIGHT // 2 + 80)

    def draw_menu(self):
        # Draw the title screen and the basic control instructions.
        text(self.logical, self.big, "ASTEROIDS",
             C.WIDTH // 2 - 150, 180)
        text(self.logical, self.font,
             "Setas: virar/acelerar  Espaço: tiro  Shift: hiper",
             160, 300)
        text(self.logical, self.font,
             "Pressione qualquer tecla...", 260, 360)
