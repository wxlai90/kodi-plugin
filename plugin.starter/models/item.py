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
        self.to_play = kargs['to_play'] if 'to_play' in kargs else None

        # params and to_play should be mutually exclusive
        if self.params and self.to_play:
            raise Exception(
                'Exactly one of either "params" or "to_play" has to be defined. Both are defined.')

        if self.params == None and self.to_play == None:
            raise Exception(
                'Exactly one of either "params" or "to_play" has to be defined. None is defined.')

    class ItemBuilder:
        def __init__(self) -> None:
            self._name = None
            self._description = None
            self._image = None
            self._params = None
            self._to_play = None

        def name(self, name):
            self._name = name
            return self

        def description(self, description):
            self._description = description
            return self

        def image(self, image):
            self._image = image
            return self

        def params(self, params):
            self._params = params
            return self

        def to_play(self, to_play):
            self._to_play = to_play
            return self

        def build(self):
            return Item(
                name=self._name,
                description=self._description,
                image=self._image,
                params=self._params,
                to_play=self._to_play
            )
