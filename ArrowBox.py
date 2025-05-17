import pygame
from ObjectTopDown import ObjectTopDown


class ArrowBox(ObjectTopDown):
    def __init__(self, img_list, center, anim_int=6):
        ObjectTopDown.__init__(self, img_list, anim_int)

        self.rect.center = center


    def activate(self, player):
        player.arrows += 10
        self.kill()
