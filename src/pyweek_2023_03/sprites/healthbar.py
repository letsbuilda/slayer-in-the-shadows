"""Character class from"""
import arcade


class HealthBar:
    """Health bar"""

    # pylint: disable=too-many-arguments
    def __init__(self, character, width: int = 50, height: int = 10, border: int = 3, offset: int = 10):
        self.character = character

        self.remain_bar_width = width
        self.offset = offset
        self.border = border

        self.border_bar = arcade.SpriteSolidColor(width + 2 * border, height + 2 * border, arcade.color.ASH_GREY)

        self.fill_bar = arcade.SpriteSolidColor(width, height, arcade.color.RED)

        self.remain_bar = arcade.SpriteSolidColor(width, height, arcade.color.GREEN)

        self.character.game.scene.get_sprite_list("Bars").extend([self.border_bar, self.fill_bar, self.remain_bar])

    def update_health(self):
        """Updates fill of health."""
        self.remain_bar.width = (self.character.health / self.character.max_health) * self.remain_bar_width

    def update(self):
        """Updates health bar position and health. (May impact performance)"""
        self.update_health()
        self.border_bar.bottom = self.character.top + self.offset
        self.fill_bar.bottom = self.character.top + self.offset + self.border
        self.remain_bar.bottom = self.character.top + self.offset + self.border
        self.border_bar.center_x = self.character.center_x
        self.fill_bar.center_x = self.character.center_x
        self.remain_bar.center_x = self.character.center_x - (self.remain_bar_width - self.remain_bar.width) / 2
