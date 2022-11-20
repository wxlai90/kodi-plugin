import sys
import xbmcplugin
import xbmcgui

from typing import List
from models.item import Item

_baseUrl = sys.argv[0]
_screen = xbmcplugin
_handle = int(sys.argv[1])


def _formatDestination(kwargs):
    '''
        Formats and return query string based on key-value args passed in.
        Path prop is mandatory.
    '''
    params = ''

    for k, v in kwargs.items():
        params += f'&{k}={v}'

    # additional # needed for qsl to be recognized properly
    return f'{_baseUrl}#?{params}'


def action(**kwargs):
    '''
        decorator
        @params results_in, for now only screen
    '''
    results_in = kwargs['results_in']

    def my_decorator(func):
        def wrapper(*args, **kwargs):
            items, title = func(*args, **kwargs)

            if results_in == 'screen':
                createScreen(items, title)

            return items
        return wrapper
    return my_decorator


def createScreen(items: List[Item], screenTitle: str = None) -> None:
    ''' Takes in a List of Item DTO and creates a screen with them '''

    # sets the title
    _screen.setPluginCategory(
        _handle, screenTitle if screenTitle else 'Default Title')

    # sets the type, blanket videos for all videos type
    _screen.setContent(_handle, 'videos')

    # create a list of items and add to screen
    listItems = []

    for item in items:
        listItem = xbmcgui.ListItem()
        listItem.setLabel(item.name)
        listItem.setInfo('video', {
            'plot': item.description
        })

        if item.image:
            listItem.setArt({
                'thumb': item.image,
                'icon': item.image,
                'fanart': item.image
            })

        # it's a string of true or false because of kodi's official api
        listItem.setProperty(
            'IsPlayable', 'false' if item.isFolder else 'true')

        url = _formatDestination(item.params)
        listItems.append((url, listItem, False))

    _screen.addDirectoryItems(_handle, listItems)

    # finish populating screen
    # _handle, succeeded, updateListing, cacheToDisc
    # sane defaults: True, False, False
    _screen.endOfDirectory(_handle, True, False, False)
