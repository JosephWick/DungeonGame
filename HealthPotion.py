import pygame
from ObjectTopDown import ObjectTopDown


class HealthPotion(ObjectTopDown):
    def __init__(self, img_list, center, anim_int=6):
        ObjectTopDown.__init__(self, img_list, anim_int)

        self.rect.center = center
    
    def activate(self, player):
        if player.current_health < player.max_health:
            player.current_health += 10
            self.kill()

