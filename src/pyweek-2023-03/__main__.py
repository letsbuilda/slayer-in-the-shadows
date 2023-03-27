"""Platformer Template"""

import arcade

from .assets import get_tile_map_path
from .constants import (
    DEFAULT_DAMPING,
    GRAVITY,
    PLAYER_FRICTION,
    PLAYER_JUMP_IMPULSE,
    PLAYER_MASS,
    PLAYER_MAX_HORIZONTAL_SPEED,
    PLAYER_MAX_VERTICAL_SPEED,
    PLAYER_MOVE_FORCE_IN_AIR,
    PLAYER_MOVE_FORCE_ON_GROUND,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    TILE_SCALING,
)
from .sprites.enemy import DemoEnemy
from .sprites.player import Player


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(
            SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True
        )

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
        self.up_key_down = False
        self.left_key_down = False
        self.right_key_down = False

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Setup the Cameras
        self.camera_sprites = arcade.Camera(self.width, self.height)
        self.camera_gui = arcade.Camera(self.width, self.height)

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
            self.tile_map = arcade.load_tilemap(
                map_path, TILE_SCALING, layer_options
            )

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        for spawner in self.scene.get_sprite_list("Spawners"):
            entity_id = spawner.properties["tile_id"]
            if entity_id == 0:
                self.player = Player(spawner.bottom, spawner.left)
                self.scene.add_sprite("Player", self.player)
            elif entity_id == 1:
                self.scene.add_sprite(
                    "Enemy", DemoEnemy(spawner.bottom, spawner.left)
                )

        self.scene.remove_sprite_list_by_name("Spawners")

        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Keep track of the score
        self.score = 0

        # --- Other stuff
        # Create the 'physics engine'
        self.physics_engine = arcade.PymunkPhysicsEngine(
            (0, -GRAVITY), damping=DEFAULT_DAMPING
        )
        self.physics_engine.add_sprite(
            self.player,
            friction=PLAYER_FRICTION,
            mass=PLAYER_MASS,
            moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
            max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED,
        )
        self.physics_engine.add_sprite_list(
            self.scene["Enemy"],
            friction=PLAYER_FRICTION,
            mass=PLAYER_MASS,
            collision_type="player",
        )
        self.physics_engine.add_sprite_list(
            self.scene["Blocks"],
            body_type=1,
            friction=1,
            damping=DEFAULT_DAMPING,
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera_sprites.use()

        # Draw our Scene
        # Note, if you want pixelated look, add pixelated=True to the parameters
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.camera_gui.use()

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
        # Calculate speed based on the keys pressed

        is_on_ground = self.physics_engine.is_on_ground(self.player)
        # Update player forces based on keys pressed
        if self.left_key_down and not self.right_key_down:
            # Create a force to the left. Apply it.
            if is_on_ground:
                force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (-PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player, force)

            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player, 0)

        elif self.right_key_down and not self.left_key_down:
            # Create a force to the right. Apply it.
            if is_on_ground:
                force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player, force)

            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player, 0)
        else:
            # Player's feet are not moving. Therefore, up the friction so we stop.
            self.physics_engine.set_friction(self.player, 1.0)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        # Jumpd
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.is_on_ground(self.player):
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player, impulse)

        # Left
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = True
            self.update_player_speed()

        # Right
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_key_down = False

    def center_camera_to_player(self):
        # Find where player is, then calculate lower left corner from that
        screen_center_x = self.player.center_x - (
            self.camera_sprites.viewport_width / 2
        )
        screen_center_y = self.player.center_y - (
            self.camera_sprites.viewport_height / 2
        )

        # Set some limits on how far we scroll
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        # Here's our center, move to it
        player_centered = screen_center_x, screen_center_y
        self.camera_sprites.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        self.physics_engine.step()

        # Position the camera
        self.center_camera_to_player()

        # Update everything in the scene
        self.scene.on_update()

        self.update_player_speed()

    def on_resize(self, width, height):
        """Resize window"""
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
