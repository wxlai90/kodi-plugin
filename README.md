# kodi-plugin

Starter for kodi plugin development

## Controller

### Create a controller class and annotate it with @Controller to register it into the router

```python
@Controller
class MainController:
    ...
```

### Create a new screen to be rendered with @Action within the controller class

```python
    @action(results_in="screen")
    def landing_screen(params=None):
        items = [
            Item(name="Go to another screen", description="Some description", params={'path': 'another_screen'}),
            Item(name="Play a video",
                 description="..", to_play='$video_url')
        ]

        # Item[] Items
        return items
```

## Item DTO

Each Item object represents a selection in the screen, name and description fields are mandatory, the rest are optional.

\*More fields from the official Kodi API can be set manually.

### Summary

Feel free to add in more custom models as needed.

For an example plugin using this setup, refer to my [MeWatch Kodi Plugin](https://github.com/wxlai90/mewatch-sg/)
.
