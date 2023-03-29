"""Platformer Template"""

from itertools import zip_longest

import arcade
import arcade.gui

from .constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from .game_view import GameView


class StartView(arcade.View):
    """Start view"""

    def __init__(self):
        super().__init__()
        # Required for all code that uses UI element
        # a UIManager to handle the UI
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        self.title_text = arcade.Text(
            "NINJA GAME",
            self.window.width / 2,
            self.window.height * 3 / 4,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )

        # Make buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        # Add functionality
        @start_button.event("on_click")
        def on_click_start(event):
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        @settings_button.event("on_click")
        def on_click_settings(event):
            self.manager.disable()
            settings_view = SettingsView()
            self.window.show_view(settings_view)

        @quit_button.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_show_view(self):
        """This is run once when we switch to this view"""
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # to reset the viewport back to the start, so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """Called when this view should draw"""
        self.clear()
        self.title_text.draw()
        self.manager.draw()


class SettingsView(arcade.View):
    """Settings view"""

    def __init__(self):
        super().__init__()
        # Required for all code that uses UI element
        # a UIManager to handle the UI
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        self.fs_button = arcade.gui.UIFlatButton(text="Make fullscreen", width=200)
        self.v_box.add(self.fs_button.with_space_around(bottom=20))

        # IDK what this is meant to do so this is just placeholder for now
        self.audio_button = arcade.gui.UIFlatButton(text="Audio button", width=200)
        self.v_box.add(self.audio_button.with_space_around(bottom=20))

        keys = [
            ("Jump", "W", "UP_ARROW", "SPACE"),
            ("Left ", "L", "LEFT_ARROW"),
            ("Right", "R", "RIGHT_ARROW"),
            ("Dash", "SHIFT"),
        ]
        actions, *keybinds = zip_longest(*keys, fillvalue="")
        key_box = arcade.gui.UIBoxLayout(vertical=False)
        # Action box
        action_box = arcade.gui.UIBoxLayout(size_hint=0.8)
        for action in actions:
            action_box.add(
                arcade.gui.UILabel(text=action, font_size=30, text_color=arcade.color.BLACK).with_space_around(
                    bottom=20
                )
            )
        key_box.add(action_box.with_space_around(left=10, right=10))

        # Keybinds
        # Need to add actual functionality to switch keybinds later
        for column in keybinds:
            column_box = arcade.gui.UIBoxLayout(size_hint=0.1)
            for keybind in column:
                column_box.add(arcade.gui.UIFlatButton(text=keybind, width=200).with_space_around(bottom=20))
            key_box.add(column_box.with_space_around(left=10, right=10))

        self.v_box.add(key_box.with_space_around(bottom=20))

        @self.fs_button.event("on_click")
        def on_flip_fullscreen(event):
            self.window.set_fullscreen(not self.window.fullscreen)
            self.fs_button.text = ({self.fs_button.text} ^ {"Make fullscreen", "Minimize screen"}).pop()

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

        return_button = arcade.gui.UIFlatButton(text="<-", width=100)
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="top", child=return_button))

        @return_button.event("on_click")
        def on_click_return(event):
            self.manager.disable()
            start_view = StartView()
            self.window.show_view(start_view)

    def on_show_view(self):
        """This is run once when we switch to this view"""
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """Called when this view should draw"""
        self.clear()
        self.manager.draw()


def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
