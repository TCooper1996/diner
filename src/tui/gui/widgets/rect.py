import pygame


class Rect:
    def __init__(self, rect: pygame.Rect):
        self.rect=rect

    @property
    def x(self) -> int:
        return self.rect.x

    @property
    def y(self) -> int:
        return self.rect.y

    @property
    def width(self) -> int:
        return self.rect.width
    
    @property
    def height(self) -> int:
        return self.rect.height
    
    @property
    def bottom(self) -> int:
        return self.rect.bottom
    
    @property
    def top(self) -> int:
        return self.rect.top

    @classmethod
    def new_static(cls, x: int=0, y: int=0, width: int=0, height: int=0) -> 'Rect':
        return cls(pygame.Rect(x, y, width, height))


    def new(self, x: int | None =None, y : int | None = None, width: int | None = None, height: int | None = None):
        x = x if x else self.rect.x
        y = y if y else self.rect.y
        height = height if height else self.rect.height
        width = width if width else self.rect.width
        return pygame.Rect(left=x, top=y, width=width, height = height)




