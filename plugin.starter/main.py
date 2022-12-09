import sys

from lib import router
# initialize
from screens.main_screen import *


def main():
    router.default_name = 'Kodi Plugin'
    if sys.argv[2] == '':
        router.handle_landing()
        return

    router.handle(sys.argv[2])


main()
