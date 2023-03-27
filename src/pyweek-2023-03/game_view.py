"""Game View"""


import arcade

from .assets import get_tile_map_path
from .constants import GRAVITY, TILE_SCALING
from .sprites.enemy import Enemy
from .sprites.player import Player


# pylint: disable=too-many-instance-attributes
class GameView(arcade.View):
    """Main application class."""

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera_sprites = None

        # A non-scrolling camera that can be used to draw GUI elements
        self.camera_gui = None

        # Keep track of the score
        self.score = 0

        # What key is pressed down?
        self.left_key_down = False
        self.right_key_down = False
        self.shift_key_down = False

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Setup the Cameras
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        # Name of map file to load

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Blocks": {
                "use_spatial_hash": True,
            }
        }

        # Read in the tiled map
        with get_tile_map_path("demo") as map_path:
            self.tile_map = arcade.load_tilemap(map_path, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        for spawner in self.scene.get_sprite_list("Spawners"):
            entity_id = spawner.properties["tile_id"]
            if entity_id == 0:
                self.player = Player(spawner.bottom, spawner.left, "player/realistic_player", 100, 30, None, self)
                self.scene.add_sprite("Player", self.player)
            elif entity_id == 1:
                self.scene.add_sprite(
                    "Enemy", Enemy(spawner.bottom, spawner.left, "enemies/realistic_enemy", 100, 20, None, self)
                )

        self.scene.remove_sprite_list_by_name("Spawners")

        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Keep track of the score
        self.score = 0

        # --- Other stuff
        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=GRAVITY, walls=self.scene["Blocks"]
        )

        self.player.setup_player()

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera_sprites.use()

        # Draw our Scene
        # Note, if you a want pixelated look, add pixelated=True to the parameters
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.camera_gui.use()

        self.player.update_animation()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            start_x=10,
            start_y=10,
            color=arcade.csscolor.WHITE,
            font_size=18,
        )

    def update_player_speed(self):
        """Calculate speed based on the keys pressed"""
        self.player.update_player_speed()

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed."""
        self.player.on_key_press(symbol)

    def on_key_release(self, symbol, modifiers):
        """Called when the user releases a key."""
        self.player.on_key_release(symbol)

    def center_camera_to_player(self):
        """Centers the camera to the player"""
        # Find where player is, then calculate lower left corner from that
        screen_center_x = self.player.center_x - (self.camera_sprites.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera_sprites.viewport_height / 2)

        # Set some limits on how far we scroll
        screen_center_x = max(screen_center_x, 0)
        screen_center_y = max(screen_center_y, 0)

        # Here's our center, move to it
        player_centered = screen_center_x, screen_center_y
        self.camera_sprites.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        self.center_camera_to_player()

    def on_resize(self, width, height):
        """Resize window"""
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))
