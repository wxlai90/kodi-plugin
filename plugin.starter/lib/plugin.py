import sys
import urllib.parse
import inspect
from typing import Callable, Dict, Any, Optional, List, Union
import xbmc
import xbmcgui
import xbmcplugin
from models.item import Item
from models.playable import Playable
from models.screen import Screen

class Plugin:
    def __init__(self, argv: List[str]):
        self.url = argv[0]
        self.handle = int(argv[1])
        self.args = urllib.parse.parse_qs(argv[2][1:]) # Remove '?'
        
        self.routes: Dict[str, Callable] = {}
        self.playables: set = set()
        
    def route(self, path_or_func: Union[str, Callable] = None):
        """
        Decorator to register a route.
        Can be used as @plugin.route (no parens), @plugin.route() (parens), or @plugin.route('name').
        """
        def decorator(func: Callable, path: str = None):
            actual_path = path if path else func.__name__
            if actual_path in self.routes:
                raise Exception(f"Route '{actual_path}' already registered.")
            self.routes[actual_path] = func
            return func

        if callable(path_or_func):
            # Used as @plugin.route without parens
            return decorator(path_or_func)
        else:
            # Used as @plugin.route('path') or @plugin.route()
            def wrapper(func):
                return decorator(func, path_or_func)
            return wrapper

    def landing(self):
        """Decorator to register the landing screen."""
        return self.route('/')

    def playable(self, func: Callable):
        """Decorator to register a playable item handler."""
        path = func.__name__
        if path in self.routes:
            raise Exception(f"Route '{path}' already registered.")
        self.routes[path] = func
        self.playables.add(path)
        func._is_playable = True
        return func

    def run(self):
        """Dispatch the request."""
        # Check if we have a path in args, otherwise it's landing
        # Note: Standard kodi params often use 'mode' or just path. 
        # The previous router used 'path'. We will stick to 'path' for now.
        # If args is empty or path not present, default to landing '/'
        
        path_list = self.args.get('path')
        path = path_list[0] if path_list else '/'

        if path not in self.routes:
            xbmcgui.Dialog().notification('Error', f'No handler for path: {path}')
            return

        handler = self.routes[path]
        
        # Flatten args: {'key': ['val']} -> {'key': 'val'}
        request_params = {k: v[0] for k, v in self.args.items()}
        
        # Auto-inject parameters based on signature
        sig = inspect.signature(handler)
        has_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
        
        if has_kwargs:
            # If function accepts **kwargs, pass everything
            call_kwargs = request_params
        else:
            # Filter params to match function signature
            call_kwargs = {k: v for k, v in request_params.items() if k in sig.parameters}
        
        try:
            result = handler(**call_kwargs)
            if isinstance(result, Screen):
                self._render_screen(result)
            elif isinstance(result, Playable):
                self._play_item(result)
        except Exception as e:
            xbmcgui.Dialog().notification('Error', str(e))
            xbmc.log(f"Plugin Error: {e}", level=xbmc.LOGERROR)

    def url_for(self, func_or_path: Union[str, Callable], **kwargs) -> str:
        """Generate a URL for a route."""
        if callable(func_or_path):
            path = func_or_path.__name__
        else:
            path = func_or_path
            
        kwargs['path'] = path
        query = urllib.parse.urlencode(kwargs)
        return f"{self.url}?{query}"

    def _play_item(self, playable: Playable):
        list_item = xbmcgui.ListItem(path=playable.url)
        list_item.setSubtitles(playable.subtitles)
        xbmcplugin.setResolvedUrl(self.handle, True, list_item)

    def _render_screen(self, screen: Screen):
        xbmcplugin.setPluginCategory(self.handle, screen.screen_name)
        xbmcplugin.setContent(self.handle, 'videos')

        items = []
        for item in screen.items:
            list_item = xbmcgui.ListItem(label=item.name)
            list_item.setInfo('video', {'plot': item.description})
            
            if item.image:
                list_item.setArt({
                    'thumb': item.image,
                    'icon': item.image,
                    'fanart': item.image
                })

            # Check if target is playable
            # We rely on the Item to know if it's playable (auto-detected from handler)
            is_folder = not item.is_playable
            
            if item.is_playable:
                list_item.setProperty('IsPlayable', 'true')
            
            # Construct URL
            # Merge path into the query params
            query_params = {'path': target_path}
            query_params.update(item.kwargs)
            
            url_query = urllib.parse.urlencode(query_params)
            url = f"{self.url}?{url_query}"
            
            items.append((url, list_item, is_folder))

        xbmcplugin.addDirectoryItems(self.handle, items)
        xbmcplugin.endOfDirectory(self.handle)


# Global instance initialized with Kodi's sys.argv
# This is safe because each Kodi call is a fresh process.
plugin = Plugin(sys.argv)

