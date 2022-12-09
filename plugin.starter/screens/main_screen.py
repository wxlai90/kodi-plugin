from lib.router import action, landing_action
from models.item import Item
from models.screen import Screen


@landing_action
def landing_screen(params=None):
    item = Item.ItemBuilder().name("Another screen").description(
        "Some description").params({'path': 'another_screen'}).build()

    screen = Screen([item], 'Select a show')
    return screen


@action
def another_screen(params=None):
    items = [
        Item.ItemBuilder().name("Play a video").description(
            "Some description").to_play("https://www.w3schools.com/html/mov_bbb.mp4'").build()
    ]

    screen = Screen(items, 'Select a show')
    return screen
