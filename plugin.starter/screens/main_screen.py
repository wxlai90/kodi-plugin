import xbmc
import xbmcgui
from lib.plugin import plugin
from models.item import Item
from models.playable import Playable
from models.screen import Screen


@plugin.landing()
def my_landing():
    items = [
        Item.create(
            name="Categories",
            description="Browse videos by category",
            handler=list_categories,
            image="https://via.placeholder.com/150"
        ),
        Item.create(
            name="Search",
            description="Search for a video",
            handler=search_video,
            image="https://via.placeholder.com/150"
        ),
        Item.create(
            name="Play Sample Video",
            description="Directly play a sample",
            handler=resolve_and_play_video,
            video_id='sample_1',
            image="https://www.w3schools.com/html/pic_trulli.jpg"
        ),
    ]

    return Screen(items, 'My Plugin Home')


@plugin.route
def list_categories():
    # In a real app, you might fetch these from an API
    categories = ['Action', 'Comedy', 'Documentary']
    
    items = []
    for cat in categories:
        items.append(Item.create(
            name=cat,
            handler=list_videos_by_category,
            category_name=cat
        ))
        
    return Screen(items, 'Categories')


@plugin.route
def list_videos_by_category(category_name):
    # Simulate fetching videos for a category
    items = [
        Item.create(
            name=f"{category_name} Video 1",
            handler=resolve_and_play_video,
            video_id=f"{category_name}_1"
        ),
        Item.create(
            name=f"{category_name} Video 2",
            handler=resolve_and_play_video,
            video_id=f"{category_name}_2"
        ),
    ]
    return Screen(items, f"Videos in {category_name}")


@plugin.route
def search_video():
    keyboard = xbmc.Keyboard('', 'Search for a video')
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        query = keyboard.getText()
        # Return a screen with results for the query
        return search_results(query=query)
    
    # If cancelled, return to previous screen (returning None does this implicitly in Kodi)
    return None


@plugin.route
def search_results(query):
    # Fake search results
    items = [
        Item.create(
            name=f"Result for '{query}'",
            handler=resolve_and_play_video,
            video_id=f"search_{query}"
        )
    ]
    return Screen(items, f"Search: {query}")


@plugin.playable
def resolve_and_play_video(video_id='0'):
    xbmcgui.Dialog().notification('Playing', f'Video ID: {video_id}')
    url = resolve_stream(video_id)
    return Playable(url=url)


def resolve_stream(video_id):
    # do some resolving logic using video_id
    # For demo, returning a sample video
    return "https://www.w3schools.com/html/mov_bbb.mp4"
