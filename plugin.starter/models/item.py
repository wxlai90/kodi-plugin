from dataclasses import dataclass, field
from typing import Dict, Optional, Union, Callable, Any


@dataclass
class Item:
    name: str
    path: str
    kwargs: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    image: Optional[str] = None
    is_playable: bool = False

    @classmethod
    def create(cls, name: str, handler: Union[str, Callable], description: str = "", image: str = None, is_playable: bool = None, **kwargs):
        """
        Factory method to create an Item with a handler function and arguments.
        
        :param name: Label of the item
        :param handler: The function (or string name) that handles the click
        :param description: Description of the item
        :param image: URL or path to the image
        :param is_playable: Explicitly set if the item is playable. If None, detects from handler.
        :param kwargs: Arguments to pass to the handler (e.g., video_id='123')
        """
        path = handler.__name__ if callable(handler) else str(handler)
        
        if is_playable is None:
             is_playable = getattr(handler, '_is_playable', False) if callable(handler) else False
             
        return cls(name=name, path=path, kwargs=kwargs, description=description, image=image, is_playable=is_playable)
