# kodi-plugin

Starter for kodi plugin development

### Create a landing screen by decorating it with @landing_screen.

This should only be defined once and serves as the entry point into the plugin.

```python
@landing_screen
def my_landing(params=None):
    items = [
        Item.ItemBuilder()
        .name("An Item")
        .description("Some description")
        .params(Params().path(another_screen))
        .playable()
        .build(),
    ]

    screen = Screen(items, 'Select a show')
    return screen
```

### Create a new screen to be rendered with @screen

```python
@screen
def another_screen(params=None):
    items = [
        Item.ItemBuilder()
        .name("View all videos")
        .description("Some description")
        .params(Params().path(screen_that_contains_playable_items))
        .build(),
    ]

    screen = Screen(items, 'Select a show')
    return screen
```

For items that should resolve to a stream.

```python
@playable
def screen_that_contains_playable_items(params=None):
    items = [
        Item.ItemBuilder()
        .name("Select a video")
        .description("Some description")
        .params(Params().path(resolve_and_play_video))
        .playable()
        .build(),
    ]

    screen = Screen(items, 'Select a show')
    return screen
```

Use `@playable` decorator and return a `Playable` model for resolving to a stream instead of displaying a new screen.

```python
@playable
def resolve_and_play_video(params=None):
    url = resolveStream()

    playable = Playable.PlayableBuilder()\
    .url(url)
    .build()

    return playable


def resolveStream():
    # do some resolving logic

    return "https://www.w3schools.com/html/mov_bbb.mp4"

```

## Screen DTO

Each `Screen` holds information about what to render on screen, this includes screen title and the items to be shown.

## Item DTO

Each `Item` object represents a selection in the screen, name and description fields are mandatory, the rest are optional.

\*More fields from the official Kodi API can be set manually.

## Params DTO

Params is internally represented as a dictionary of `Item`, this `Params` model only provides a helper method `.path()` since that is a mandatory field. It is also possible to pass in a dictionary directly.

`.path()` takes in the name of the function as a string. This provides some flexibility as the function might not be in the same package and we need not have unnecessary imports.

## Playable DTO

`Playable` is an object with `url:string` and `subtitles:string[]`.

### Summary

Feel free to add in more custom models as needed.

For an example plugin using this setup, refer to my [MeWatch Kodi Plugin](https://github.com/wxlai90/mewatch-sg/)
.
