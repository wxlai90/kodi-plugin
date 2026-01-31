import sys
import unittest
from unittest.mock import MagicMock
import os

sys.modules['xbmc'] = MagicMock()
sys.modules['xbmcgui'] = MagicMock()
sys.modules['xbmcplugin'] = MagicMock()

original_argv = sys.argv
sys.argv = ['plugin://plugin.starter', '1', '?']

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../plugin.starter'))
sys.path.insert(0, project_root)

from lib.plugin import Plugin
from models.item import Item
from models.screen import Screen
from models.playable import Playable

class TestPluginCore(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin(['plugin://test.plugin', '99', '?'])
        
        sys.modules['xbmcgui'].reset_mock()
        sys.modules['xbmcplugin'].reset_mock()

    def test_route_registration(self):
        """Test that routes are correctly registered."""
        @self.plugin.route('/foo')
        def foo():
            return "bar"
        
        self.assertIn('/foo', self.plugin.routes)
        self.assertEqual(self.plugin.routes['/foo'], foo)

    def test_route_name_inference(self):
        """Test that route path is inferred from function name if not provided."""
        @self.plugin.route
        def baz():
            pass
        
        self.assertIn('baz', self.plugin.routes)

    def test_route_collision_exception(self):
        """Test that registering a duplicate route raises an exception."""
        @self.plugin.route('/duplicate')
        def one(): pass

        with self.assertRaises(Exception) as context:
            @self.plugin.route('/duplicate')
            def two(): pass
        
        self.assertTrue("already registered" in str(context.exception))

    def test_playable_registration_and_marker(self):
        """Test that @playable registers route and sets the _is_playable marker."""
        @self.plugin.playable
        def play_me():
            pass
        
        self.assertIn('play_me', self.plugin.routes)
        self.assertIn('play_me', self.plugin.playables)
        self.assertTrue(getattr(play_me, '_is_playable', False))

    def test_playable_collision(self):
        """Test collision detection for playable routes."""
        @self.plugin.route
        def taken(): pass
        
        with self.assertRaises(Exception):
            @self.plugin.playable
            def taken(): pass

    def test_item_auto_detection_of_playable(self):
        """Test that Item.create detects the _is_playable marker."""
        @self.plugin.playable
        def my_video(): pass
        
        @self.plugin.route
        def my_folder(): pass

        item_vid = Item.create("Vid", my_video)
        item_dir = Item.create("Dir", my_folder)
        
        self.assertTrue(item_vid.is_playable)
        self.assertFalse(item_dir.is_playable)

    def test_url_for(self):
        """Test URL generation."""
        url = self.plugin.url_for('some_func', id=123, cat='action')
        self.assertTrue(url.startswith('plugin://test.plugin?'))
        self.assertIn('id=123', url)
        self.assertIn('cat=action', url)
        self.assertIn('path=some_func', url)

    def test_dispatch_simple(self):
        """Test running the plugin dispatches to the correct handler."""
        p = Plugin(['plugin://p', '1', '?path=/target&val=success'])
        
        mock_handler = MagicMock(return_value=None)
        p.routes['/target'] = mock_handler
        
        p.run()
        
        mock_handler.assert_called_once_with(val='success')

    def test_dispatch_landing(self):
        """Test defaulting to landing page if no path."""
        p = Plugin(['plugin://p', '1', '']) # Empty query
        
        mock_landing = MagicMock(return_value=None)
        p.routes['/'] = mock_landing
        
        p.run()
        
        mock_landing.assert_called_once()

    def test_render_screen_playable_property(self):
        """Test that _render_screen sets IsPlayable property correctly."""
        item_play = Item(name="Play", path="play", is_playable=True)
        item_dir = Item(name="Dir", path="dir", is_playable=False)
        screen = Screen(items=[item_play, item_dir], screen_name="Home")
        
        mock_add_items = sys.modules['xbmcplugin'].addDirectoryItems
        
        self.plugin._render_screen(screen)
        
        self.assertTrue(mock_add_items.called)
        call_args = mock_add_items.call_args[0]
        items_list = call_args[1]
        
        url_1, list_item_1, is_folder_1 = items_list[0]
        self.assertFalse(is_folder_1, "Playable item should have isFolder=False")
  
        url_2, list_item_2, is_folder_2 = items_list[1]
        self.assertTrue(is_folder_2, "Standard item should have isFolder=True")

if __name__ == '__main__':
    unittest.main()