import pygame
from ObjectTopDown import ObjectTopDown


class GoldCoin(ObjectTopDown):
    def __init__(self, img_list, center, anim_int=6):
        ObjectTopDown.__init__(self, img_list, anim_int)

        self.rect.center = center


    def activate(self, player):
        player.gold += 1
        self.kill()
