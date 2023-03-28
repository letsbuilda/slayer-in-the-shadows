"""Platformer Template"""

import arcade

from .constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from .views import StartView


def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
