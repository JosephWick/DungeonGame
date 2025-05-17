import pygame
from ObjectTopDown import ObjectTopDown
from Bullet import Bullet


class Enemy(ObjectTopDown):
    def __init__(self, img_list, center, anim_int=3, arrow_freq=30, bullet_speed=12):
        ObjectTopDown.__init__(self, img_list, anim_int)

        self.rect.center = center

        self.arrow_cooldown = 0
        self.hasLoS = False
        self.arrow_freq = arrow_freq

        self.bullet_speed=bullet_speed

        self.do_anim = False


    def update(self, uvx, uvy, player, walls_group, bullet_img, bullets_group):
        self.move(uvx, uvy)

        self.hasLoS = self.hasLineOfSight(player, walls_group)

        # if clear line of sight to player, shoot player
        if self.hasLoS and self.arrow_cooldown == 0:
            bullets_group.add(Bullet(bullet_img, self.rect.center,
                                     player.rect.center, self.bullet_speed))
            self.arrow_cooldown = self.arrow_freq
            self.do_anim = True
            self.dt = self.anim_int - 1

        if self.arrow_cooldown > 0:
            self.arrow_cooldown -= 1

        if self.do_anim:
            self.idle_animate()
            if self.image_idx == 0:
                self.do_anim = False

        # if clear line of sight to player, face player
        if self.hasLoS:
            self.pointAt(player.rect.center)
        # else keep prior angle
        else:
            self.image = pygame.transform.rotate(self.image_list[self.image_idx], self.angle)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(center=self.rect.center)


    def hasLineOfSight(self, player, walls_group):
        hasLineOfSight = True
        for wall in walls_group.sprites():
            if wall.rect.clipline(player.rect.center, self.rect.center):
                return False

        return True
