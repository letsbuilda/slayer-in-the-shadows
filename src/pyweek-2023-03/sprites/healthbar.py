"""Character class from"""
import arcade


class HealthBar:
    """Health bar"""

    # pylint: disable=too-many-arguments
    def __init__(self, character, width: int = 50, height: int = 10, border: int = 3, offset: int = 10):
        self.character = character

        self.fill_bar_width = width
        self.offset = offset
        self.border = border

        self.border_bar = arcade.SpriteSolidColor(width + 2 * border, height + 2 * border, arcade.color.ASH_GREY)

        self.fill_bar = arcade.SpriteSolidColor(width, height, arcade.color.GREEN)

        self.character.game.scene.get_sprite_list("Bars").extend([self.border_bar, self.fill_bar])

    def update_health(self):
        """Updates fill of health."""
        self.fill_bar.width = (self.character.health / self.character.max_health) * self.fill_bar_width

    def update(self):
        """Updates health bar position. (May impact performance)"""
        self.border_bar.bottom = self.character.top + self.offset - self.border
        self.fill_bar.bottom = self.character.top + self.offset
        self.border_bar.left = self.character.left - (self.fill_bar_width/4) + self.border
        self.fill_bar.left = self.character.left - (self.fill_bar_width/4)
