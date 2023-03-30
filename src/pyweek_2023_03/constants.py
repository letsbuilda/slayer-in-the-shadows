"""Variables that are needed in multiple files and don't change."""
import arcade

# Screen
SCREEN_WIDTH = 24 * 64
SCREEN_HEIGHT = 15 * 64
SCREEN_TITLE = "pyweek-2023-03"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Dash
MAX_DASHES = 1
DASH_COOLDOWN = 2

# Time slow
SLOW_TIME_DURATION = 4
SLOW_TIME_COOLDOWN = 1

ENEMY_RENDER_DISTANCE = 500
ENEMY_FOV = 0.4
FRAMES_PER_RAYCAST = 5

# --- Physics forces. Higher number, faster accelerating.

# Gravity
GRAVITY = 3_000

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 1.0

# Friction between objects
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

# Mass (defaults to 1)
PLAYER_MASS = 2.0

# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1_600
PLAYER_MOVE_FORCE_ON_GROUND = 30_000
PLAYER_MOVE_FORCE_IN_AIR = 10_000
PLAYER_JUMP_IMPULSE = 1800
DASH_MOVE_IMPULSE = 15_000

# Controls
KEYMAP_DICT = {
    "Jump": [arcade.key.W, arcade.key.UP, arcade.key.SPACE],
    "Left": [arcade.key.A, arcade.key.LEFT],
    "Right": [arcade.key.D, arcade.key.RIGHT],
    "Dash": [arcade.key.L, arcade.key.MOD_SHIFT],
    "Slow time": [arcade.key.P]
}
ARCADE_KEYS_TO_NAME = {
    arcade.key.W: "W",
    arcade.key.UP: "UP_ARROW",
    arcade.key.SPACE: "SPACE",
    arcade.key.A: "A",
    arcade.key.LEFT: "LEFT_ARROW",
    arcade.key.D: "D",
    arcade.key.RIGHT: "RIGHT_ARROW",
    arcade.key.L: "L",
    arcade.key.MOD_SHIFT: "MOD_SHIFT",
    arcade.key.P: "P"
}

ANIMATION_FREEZE_TIME = 3