import pygame
from ObjectTopDown import ObjectTopDown


class Wall(ObjectTopDown):

    def __init__(self, img, center):
        ObjectTopDown.__init__(self, [img])
        self.rect.center = center


