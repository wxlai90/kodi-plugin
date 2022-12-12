from lib.router import action, landing_action
from models.item import Item
from models.params import Params
from models.playable import Playable
from models.screen import Screen


@landing_action
def landing_screen(params=None):
    items = [Item.ItemBuilder().name("Select a video").description(
        "Some description").params(Params().path(resolve_and_play_video)).playable().build(),
    ]

    screen = Screen(items, 'Select a show')
    return screen


@action
def resolve_and_play_video(params=None):
    url = resolveStream()

    playable = Playable.PlayableBuilder().url(url).build()

    return playable


def resolveStream():
    # do some resolving logic

    return "https://www.w3schools.com/html/mov_bbb.mp4"
