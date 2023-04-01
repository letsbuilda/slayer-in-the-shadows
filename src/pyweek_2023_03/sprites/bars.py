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


class ChargeBar:
    """ Attack charge bar """
    def __init__(self, character, width: int = 10, height: int = 40, offset: int = 10):
        self.character = character

        self.full_bar_height = height
        self.width = width
        self.offset = offset

        self.fill_bar = arcade.SpriteSolidColor(width, height, arcade.color.RICH_BLACK)
        self.half_charge_indicator = arcade.SpriteSolidColor(width, 3, arcade.color.CADMIUM_ORANGE)
        self.charge_bar = arcade.SpriteSolidColor(width, 1, arcade.color.BANANA_YELLOW)

        self.bar_display = False

    def update_charge(self):
        """ Updates charge progress """
        if self.character.is_charging_attack:
            self.charge_bar.height = self.full_bar_height * min(self.character.charge_duration / 3, 1) + 0.1
            if not self.bar_display:
                self.character.game.scene.get_sprite_list('Bars').extend(
                    [self.fill_bar, self.charge_bar, self.half_charge_indicator]
                )
                self.bar_display = True
        else:
            self.charge_bar.height = 0.1
            if self.bar_display:
                self.character.game.scene.get_sprite_list('Bars').remove(self.fill_bar)
                self.character.game.scene.get_sprite_list('Bars').remove(self.charge_bar)
                self.character.game.scene.get_sprite_list('Bars').remove(self.half_charge_indicator)
                self.bar_display = False

    def update(self):
        """ Updates charge bar """
        self.update_charge()
        self.fill_bar.left = self.character.right + self.offset
        self.fill_bar.center_y = self.character.center_y

        self.half_charge_indicator.left = self.character.right + self.offset
        self.half_charge_indicator.center_y = self.character.center_y - self.full_bar_height / 6

        self.charge_bar.left = self.character.right + self.offset
        self.charge_bar.center_y = self.character.center_y - (self.full_bar_height - self.charge_bar.height) / 2
