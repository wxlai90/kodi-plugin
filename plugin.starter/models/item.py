class Item:
    def __init__(self, **kargs) -> None:
        '''
            name:str
            description:str
            image: str
            params:dict
        '''
        self.name = kargs['name']
        self.description = kargs['description']
        self.image = kargs['image'] if 'image' in kargs else None
        self.params = kargs['params'] if 'params' in kargs else None
        self.playable = kargs['playable'] if 'playable' in kargs else False

        # params and to_play should be mutually exclusive
        if not self.params:
            raise Exception('Params must be defined')

    class ItemBuilder:
        def __init__(self) -> None:
            self._name = None
            self._description = None
            self._image = None
            self._params = {}
            self._playable = False

        def name(self, name):
            self._name = name
            return self

        def description(self, description):
            self._description = description
            return self

        def image(self, image):
            self._image = image
            return self

        def params(self, key, value):
            self._params[key] = value
            return self

        def playable(self, b=True):
            self._playable = b
            return self

        def build(self):
            return Item(
                name=self._name,
                description=self._description,
                image=self._image,
                params=self._params,
                playable=self._playable
            )
