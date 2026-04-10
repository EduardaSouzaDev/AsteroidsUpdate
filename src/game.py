
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
        pg.mixer.init()
        self._sfx_ship = self._load_sound(C.SFX_SHIP_BLASTER)
        self._sfx_ufo = self._load_sound(C.SFX_UFO_BLASTER)
        self._sfx_stone_big = self._load_sound(C.SFX_BIG_STONE_BREAK)
        self._sfx_stone_small = self._load_sound(C.SFX_SMALL_STONE_BREAK)
        self._sfx_defeat = self._load_sound(C.SFX_DEFEAT)
        self._intro_path_ok = C.INTRO_MUSIC.is_file()
        self._theme_path_ok = C.THEME_MUSIC.is_file()
        self._bgm_mode = "none"  # "none" | "intro" | "theme"
        if C.RANDOM_SEED is not None:
            random.seed(C.RANDOM_SEED)
        self.logical = pg.Surface((C.WIDTH, C.HEIGHT))
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        pg.display.set_caption("Asteroides")
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("consolas", 20)
        self.big = pg.font.SysFont("consolas", 48)
        self.scene = Scene("menu")
        self.world = World(
            self._sfx_ship,
            self._sfx_ufo,
            self._sfx_stone_big,
            self._sfx_stone_small,
        )
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
                        self.world = World(
                            self._sfx_ship,
                            self._sfx_ufo,
                            self._sfx_stone_big,
                            self._sfx_stone_small,
                        )
                        self.scene = Scene("play")
                        self._start_theme_music()
                    elif self.scene.name == "game_over":
                        if e.key in (pg.K_RETURN, pg.K_SPACE):
                            self.world = World(
                                self._sfx_ship,
                                self._sfx_ufo,
                                self._sfx_stone_big,
                                self._sfx_stone_small,
                            )
                            self.go_fade = 0.0
                            self.scene = Scene("play")
                            self._start_theme_music()

            keys = pg.key.get_pressed()
            self.logical.fill(C.BLACK)

            if self.scene.name == "menu":
                self._start_intro_music()
                self.draw_menu()
            elif self.scene.name == "play":
                self.world.update(dt, keys)
                self.world.draw(self.logical, self.font)
                # Verifica se o mundo sinalizou fim de jogo
                if self.world.game_over:
                    self.final_score = self.world.score
                    self.go_fade = 0.0
                    self._stop_bgm()
                    if self._sfx_defeat is not None:
                        self._sfx_defeat.play()
                    self.scene = Scene("game_over")
            elif self.scene.name == "game_over":
                self.go_fade += dt
                self.draw_game_over()

            self._present()
            pg.display.flip()

    @staticmethod
    def _load_sound(path):
        if not path.is_file():
            return None
        try:
            s = pg.mixer.Sound(str(path))
            s.set_volume(C.SFX_VOLUME)
            return s
        except pg.error:
            return None

    def _start_intro_music(self):
        if not self._intro_path_ok or self._bgm_mode == "intro":
            return
        try:
            pg.mixer.music.stop()
            pg.mixer.music.load(str(C.INTRO_MUSIC))
            pg.mixer.music.set_volume(C.MUSIC_VOLUME)
            pg.mixer.music.play(-1)
            self._bgm_mode = "intro"
        except pg.error:
            self._intro_path_ok = False

    def _start_theme_music(self):
        if self._bgm_mode == "theme":
            return
        pg.mixer.music.stop()
        if not self._theme_path_ok:
            self._bgm_mode = "none"
            return
        try:
            pg.mixer.music.load(str(C.THEME_MUSIC))
            pg.mixer.music.set_volume(C.MUSIC_VOLUME)
            pg.mixer.music.play(-1)
            self._bgm_mode = "theme"
        except pg.error:
            self._theme_path_ok = False
            self._bgm_mode = "none"

    def _stop_bgm(self):
        if self._bgm_mode != "none":
            pg.mixer.music.stop()
            self._bgm_mode = "none"

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
