# ASTEROIDE SINGLEPLAYER v1.0
# This file stores the gameplay, rendering, and balancing constants.

from pathlib import Path

_ASSET_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = _ASSET_ROOT / "assets"
INTRO_MUSIC = ASSETS_DIR / "intro-song.WAV"
THEME_MUSIC = ASSETS_DIR / "theme-song.wav"
SFX_SHIP_BLASTER = ASSETS_DIR / "blaster-ship.WAV"
SFX_UFO_BLASTER = ASSETS_DIR / "blaster-ufo.WAV"
SFX_BIG_STONE_BREAK = ASSETS_DIR / "big-stone-break.wav"
SFX_SMALL_STONE_BREAK = ASSETS_DIR / "small-stone-break.wav"
SFX_DEFEAT = ASSETS_DIR / "defeat-sound.wav"
MUSIC_VOLUME = 0.45
SFX_VOLUME = 0.65

WIDTH = 960
HEIGHT = 720
FPS = 60

START_LIVES = 3
SAFE_SPAWN_TIME = 2.0
WAVE_DELAY = 2.0

SHIP_RADIUS = 15
SHIP_TURN_SPEED = 220.0
SHIP_THRUST = 220.0
SHIP_FRICTION = 0.995
SHIP_FIRE_RATE = 0.2
SHIP_BULLET_SPEED = 420.0
SHIP_DASH_IMPULSE = 100.0
SHIP_DASH_COOLDOWN = 0.85
SHIP_DASH_ENERGY_COST = 22
SHIP_SLOW_MULT = 0.5
SHIP_SLOW_ENERGY_COST = 15
HYPERSPACE_COST = 250

AST_VEL_MIN = 30.0
AST_VEL_MAX = 90.0
AST_SIZES = {
    "L": {"r": 46, "score": 20, "split": ["M", "M"]},
    "M": {"r": 24, "score": 50, "split": ["S", "S"]},
    "S": {"r": 12, "score": 100, "split": []},
}

BULLET_RADIUS = 2
BULLET_TTL = 1.0
MAX_BULLETS = 4

UFO_SPAWN_EVERY = 15.0
UFO_SPEED = 80.0
UFO_FIRE_EVERY = 1.2
UFO_BULLET_SPEED = 260.0
UFO_BULLET_TTL = 1.8
UFO_BIG = {"r": 18, "score": 200, "aim": 0.2}
UFO_SMALL = {"r": 12, "score": 1000, "aim": 0.6}

WHITE = (240, 240, 240)
GRAY = (120, 120, 120)
BLACK = (0, 0, 0)

RANDOM_SEED = None

# Duração do fade-in da tela de game over (segundos)
GAME_OVER_FADE_DURATION = 1.5
