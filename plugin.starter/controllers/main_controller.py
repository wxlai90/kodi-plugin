from lib.action_builder import action
from models.item import Item
from lib.router import Controller


# Sample controller
@Controller
class MainController:
    '''
        Each handler function should return 2 values,
        1. list of items DTO
        2. title, None to use default
    '''

    # TODO: update items to be rendered on screen
    @action(results_in="screen")
    def landing_screen(params=None):
        items = [
            Item(name="A Kodi selection", description="Some description"),
            Item(name="Another Kodi selection",
                 description="Some more description"),
            Item(name="Yet another Kodi selection",
                 description="Even more descrition with params", params={'repeatable': True})
        ]

        # Item[] Items, String: Screen Title
        return items, None
