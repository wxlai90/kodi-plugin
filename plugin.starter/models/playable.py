class Playable:
    def __init__(self, url: str, subtitles) -> None:
        self.url = url
        self.subtitles = subtitles

    class PlayableBuilder:
        def __init__(self) -> None:
            self._url = None
            self._subtitles = []

        def url(self, url: str):
            self._url = url
            return self

        def subtitles(self, subtitles):
            self._subtitles = subtitles
            return self

        def build(self):
            return Playable(self._url, self._subtitles)
