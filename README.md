# Kodi Plugin Starter

A modern, lightweight micro-framework for building Kodi plugins (Matrix/Nexus/Omega+).

## Features

-   **Decorators for Routing**: Clean, Flask-like routing syntax (`@plugin.route`, `@plugin.landing`).
-   **Type-Safe Models**: Uses Python dataclasses for `Item`, `Screen`, and `Playable`.
-   **Auto-Injection**: Function arguments are automatically populated from URL parameters.
-   **Developer Experience**: Simple factory methods (`Item.create`) to avoid boilerplate.

## Getting Started

### 1. Define Routes

The core of the framework is the `plugin` instance. You define screens by decorating functions. 
The decorator `@plugin.route` uses the function name as the route path by default, ensuring your links always work.

#### Landing Screen

The entry point of your addon.

```python
from lib.plugin import plugin
from models.item import Item
from models.screen import Screen

@plugin.landing()
def my_landing():
    items = [
        Item.create(
            name="Browse Categories",
            handler=list_categories,
            description="View all video categories"
        ),
        Item.create(
            name="Search",
            handler=search_video
        )
    ]
    return Screen(items, 'Home')
```

#### Standard Screens

Create a screen that lists more items (folders).

```python
@plugin.route
def list_categories():
    items = [
        Item.create(name="Action", handler=list_videos, category="action"),
        Item.create(name="Comedy", handler=list_videos, category="comedy"),
    ]
    return Screen(items, 'Categories')
```

### 2. Passing Arguments

You can pass arguments to your handlers. The framework automatically injects them based on the function signature.

```python
# The 'category' argument is auto-filled from the item creation above
@plugin.route
def list_videos(category):
    # Fetch videos for this category...
    items = [
        Item.create(
            name=f"Best {category} Movie", 
            handler=play_video, 
            video_id="123"
        )
    ]
    return Screen(items, f"{category.title()} Movies")
```

### 3. Playable Items

To play a video, use the `@plugin.playable` decorator and return a `Playable` object.

```python
from models.playable import Playable

@plugin.playable
def play_video(video_id):
    # Resolve the actual stream URL here
    stream_url = "https://example.com/stream.mp4"
    
    return Playable(
        url=stream_url,
        subtitles=['https://example.com/sub.srt'] # Optional
    )
```

### 4. User Input (Search)

You can use standard Kodi dialogs.

```python
import xbmc

@plugin.route
def search_video():
    keyboard = xbmc.Keyboard('', 'Search')
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        query = keyboard.getText()
        # Redirect to results
        return search_results(query=query)

@plugin.route
def search_results(query):
    # ... return Screen with results
    pass
```

## Structure

-   `lib/plugin.py`: Core framework logic.
-   `models/`: Data structures (`Item`, `Screen`, `Playable`).
-   `screens/`: Your route handlers.
-   `main.py`: Entry point.

## Installation

1.  Copy `plugin.starter` to your Kodi addons directory (rename it to your plugin ID).
2.  Update `addon.xml` with your details.
3.  Start coding in `screens/main_screen.py`.
