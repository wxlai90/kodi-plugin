from typing import List

from models.item import Item


class Screen:
    def __init__(self, items: List[Item], screen_name: str = '') -> None:
        self.items = items
        self.screen_name = screen_name

    def set_name(self, screen_name: str) -> None:
        self.screen_name = screen_name
