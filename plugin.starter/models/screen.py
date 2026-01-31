from dataclasses import dataclass
from typing import List

from models.item import Item


@dataclass
class Screen:
    items: List[Item]
    screen_name: str = ''
