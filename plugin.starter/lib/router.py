import sys

import xbmcgui
import xbmcplugin
from models.screen import Item, Screen

_baseUrl = sys.argv[0]
_screen = xbmcplugin
_handle = int(sys.argv[1])


routes = {}
default_name = ''


def _decodeParams(query_string):
    ''' decodes params from query string '''
    ''' ?&path=something&name=okays '''
    ''' returns a key-value map of params'''
    props = query_string.split('&')

    props.pop(0)  # remove '?' first element

    params = {}

    for keyed_value in props:
        k, v = keyed_value.split('=')
        params[k] = v

    return params


def handle(query_string):
    ''' handles routing, retrieve func to call from routes and call with args '''
    params = _decodeParams(query_string)

    if params['path'] not in routes:
        raise Exception(
            'No handler registered for this path [{}]'.format(params['path']))

    func = routes[params['path']]
    # might add in logger here.
    # calls func with query_string params
    func(params)


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


def handle_landing():
    routes['__landing']()


def landing_action(func):
    def wrapper(*args, **kwargs):
        screen = func(*args, **kwargs)
        createScreen(screen)

    routes['__landing'] = wrapper


def action(func):
    def wrapper(*args, **kwargs):
        screen = func(*args, **kwargs)
        createScreen(screen)

    routes[func.__name__] = wrapper


def createScreen(screen: Screen) -> None:
    ''' Takes in a List of Item DTO and creates a screen with them '''
    items = screen.items

    # sets the title
    _screen.setPluginCategory(_handle, screen.screen_name)

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

        isFolder = True
        if item.to_play:
            isFolder = False
            url = item.to_play
        else:
            url = _formatDestination(item.params)

        listItems.append((url, listItem, isFolder))

    _screen.addDirectoryItems(_handle, listItems)

    # finish populating screen
    # _handle, succeeded, updateListing, cacheToDisc
    # sane defaults: True, False, False
    _screen.endOfDirectory(_handle, True, False, False)
