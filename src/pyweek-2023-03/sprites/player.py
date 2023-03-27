"""The player"""

import arcade
import asyncio

from ..constants import *
from ..assets import get_sprite_path
from ..sprites.character import Character


class Player(Character):
    """ The main player The player sprite is 32x26"""
    
    def setup_player(self):
        """ Setup the player """
        self.dashes = 1
        self.can_dash = True
    
    def update_animation(self, delta_time: float = 1/60):
        """ Update the animation """
        
    
    def update_player_speed(self):
        """ Calculate speed based on the keys pressed """
        self.change_x = 0

        if self.game.left_key_down and not self.game.right_key_down:
            if self.game.shift_key_down and self.can_dash and self.dashes > 0:
                self.change_x = -PLAYER_DASH_SPEED
                self.dashes -= 1
                self.can_dash = False
                asyncio.run(self.reset_dash())
            else:
                self.change_x = -PLAYER_MOVEMENT_SPEED
                
        if self.game.right_key_down and not self.game.left_key_down:
            if self.game.shift_key_down and self.can_dash and self.dashes > 0:
                self.change_x = PLAYER_DASH_SPEED
                self.dashes -= 1
                self.can_dash = False
                asyncio.run(self.reset_dash())
            else:
                self.change_x = PLAYER_MOVEMENT_SPEED
    
    async def reset_dash(self):
        """ Reset dash after 1 second """
        asyncio.sleep(1)
        self.dashes = 1
            
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        
        if self.game.physics_engine.can_jump():
            self.can_dash = True

        # Jump
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.game.physics_engine.can_jump():
                self.change_y = PLAYER_JUMP_SPEED
        
        # Dash
        # if key == arcade.key.MOD_SHIFT:
        if key == 65505:
            self.game.shift_key_down = True
            self.update_player_speed()

        # Left
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.game.left_key_down = True
            self.update_player_speed()

        # Right
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.game.right_key_down = True
            self.update_player_speed()
    
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.game.left_key_down = False
            self.update_player_speed()
            
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.game.right_key_down = False
            self.update_player_speed()
        
        if key == 65505:
            self.game.shift_key_down = False
            self.update_player_speed()