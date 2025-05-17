import os
import time
import pygame
import math
import numpy as np

from Player import Player
from Bullet import Bullet
from Wall import Wall
from HealthPotion import HealthPotion
from Enemy import Enemy

from Map import Map

pygame.init()

# window dimensions
width = 1200
height = 800 

map_dim = 1600

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

pygame.display.set_caption("My Pygame Window")

# scale settings
player_scale = 60
player_speed = 3

won = False

# load relevant images
def load_images_from_folder(folderpath, transform_size):
    images_list = []
    image_files = os.listdir(folderpath)
    image_files.sort()
    for f in image_files:
        if f[-4:] != ".png":
            continue
        image = pygame.image.load(folderpath+f).convert_alpha()
        image = pygame.transform.scale(image, transform_size)
        images_list.append(image)
    return images_list

item_size = (50,50)
player_size = (player_scale, player_scale)
hud_size=(225, 75)

imagelist_player = load_images_from_folder("images/PlayerS/", player_size)
imagelist_enemy = load_images_from_folder("images/Enemy/", player_size)

image_bullet = pygame.transform.scale(pygame.image.load("images/bullet.png"), (3,10))
image_wall = pygame.transform.scale(pygame.image.load("images/Wall.png"), (50, 50))

imagelist_coin = load_images_from_folder("images/GoldCoin/", item_size)
imagelist_arrows = load_images_from_folder("images/ArrowBox/", item_size)
imagelist_health = load_images_from_folder("images/HealthPotion/", item_size)

image_portal = pygame.image.load("images/Portal.png").convert_alpha()
image_portal = pygame.transform.scale(image_portal, player_size)

imagelist_hud = load_images_from_folder("images/HUD/", hud_size)

image_dict = {
                "wall" : image_wall,
                "coin" : imagelist_coin,
                "arrow" : imagelist_arrows,
                "health" : imagelist_health,
                "enemy" : imagelist_enemy,
                "portal" : image_portal
}

# create map
thismap = Map((map_dim, map_dim), (width,height), image_dict)
walls_group, items_group, enemies_group, portals_group = thismap.make_map("map1_grid.txt")

# create a character
player_border = (map_dim/2 - 90, map_dim/2 - 90)
player_mvbox = (map_dim/2-width/2, map_dim/2-height/2)
p = Player(imagelist_player, speed=player_speed, border=player_border, mvbox=player_mvbox)
p.rect.center = (width/2, height/2)

# background
b = pygame.image.load("images/bg.png").convert()
b = pygame.transform.scale(b, (map_dim, map_dim))
br = b.get_rect(center=(width/2, height/2))

# HUD
hud_surface = imagelist_hud[0]
hud_rect = hud_surface.get_rect()
hud_rect.x = 0
hud_rect.y = 0

font = pygame.font.Font('freesansbold.ttf', 32)


# groups
# separate player and enemy arrows for collision purposes
bullets_p_group = pygame.sprite.Group()
bullets_e_group = pygame.sprite.Group()

# loop
running = True
while running:
    clock.tick(60)

    mpos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP and p.arrow_cooldown == 0:
            new_bullet = p.shoot(mpos, image_bullet)
            if new_bullet is not None:
                bullets_p_group.add(new_bullet)

    # clear and fill screen with color
    screen.fill((0, 0, 0))

    p.update()

    # movement
    keys = pygame.key.get_pressed()
    # do x movement if no wall collisions
    p.move(up=False,
           down=False,
           left=keys[pygame.K_a],
           right=keys[pygame.K_d])

    uvx = 0
    if abs(p.ux) < p.mvboxX:
        if keys[pygame.K_a]:
            uvx += player_speed
        if keys[pygame.K_d]:
            uvx -= player_speed
    walls_group.update(uvx, 0)

    collided_sprite = pygame.sprite.spritecollideany(p, walls_group, collided=pygame.sprite.collide_mask)
    if collided_sprite:
        # undo movement
        p.move(up=False,
               down=False,
               left=keys[pygame.K_d],
               right=keys[pygame.K_a])
        walls_group.update(-1*uvx, 0)
        uvx = 0

    # do y movement if no wall collisions
    p.move(up=keys[pygame.K_w],
           down=keys[pygame.K_s],
           left=False,
           right=False)

    uvy = 0
    if abs(p.uy) < p.mvboxY:
        if keys[pygame.K_w]:
            uvy += player_speed
        if keys[pygame.K_s]:
            uvy -= player_speed
    walls_group.update(0, uvy)

    collided_sprite = pygame.sprite.spritecollideany(p, walls_group, collided=pygame.sprite.collide_mask)
    if collided_sprite:
        # undo movement
        p.move(up=keys[pygame.K_s],
               down=keys[pygame.K_w],
               left=False,
               right=False)
        walls_group.update(0, -1*uvy)
        uvy = 0

    br = br.move(uvx, uvy)
    items_group.update(uvx, uvy)
    bullets_p_group.update(uvx, uvy)
    bullets_e_group.update(uvx, uvy)
    enemies_group.update(uvx, uvy, p, walls_group, image_bullet, bullets_e_group)
    portals_group.update(uvx, uvy)

    # check for item collisions
    collided_item = pygame.sprite.spritecollide(p, items_group, False, collided=pygame.sprite.collide_mask)
    for ci in collided_item:
        ci.activate(p)

    # delete any bullets that have collided with walls
    for bullet in bullets_p_group.sprites():
        if pygame.sprite.spritecollideany(bullet, walls_group):
            bullet.kill()
    for bullet in bullets_e_group.sprites():
        if pygame.sprite.spritecollideany(bullet, walls_group):
            bullet.kill()

    # check player for bullet collisions
    collided_items = pygame.sprite.spritecollide(p, bullets_e_group, True, collided=pygame.sprite.collide_mask)
    for bull in collided_items:
        p.current_health -= p.dmg_amnt

    # check enemies for bullet collisions
    for enemy in enemies_group:
        collided_items = pygame.sprite.spritecollide(enemy, bullets_p_group, 
                                                     True, collided=pygame.sprite.collide_mask)
        if len(collided_items) > 0:
            enemy.kill()

    # check player for portal collision
    collided = pygame.sprite.spritecollideany(p, portals_group,
                                              collided=pygame.sprite.collide_mask)
    if collided:
        won = True
        running = False

    # draw background
    screen.blit(b, br)

    # draw our blob
    items_group.draw(screen)
    screen.blit(p.image, p.rect)

    walls_group.draw(screen)

    bullets_p_group.draw(screen)
    bullets_e_group.draw(screen)

    enemies_group.draw(screen)

    portals_group.draw(screen)

    # draw the hud
    idx_hud = int(3-p.current_health/10)
    hud_surface = imagelist_hud[min(idx_hud,2)]
    screen.blit(hud_surface, hud_rect)

    text_arrow = font.render(str(p.arrows), True, (0,0,0))
    text_arrow_rect = text_arrow.get_rect()
    text_arrow_rect.center = (120, 40)
    screen.blit(text_arrow, text_arrow_rect)

    text_gold = font.render(str(p.gold), True, (0,0,0))
    text_gold_rect = text_arrow.get_rect()
    text_gold_rect.center = (195, 40)
    screen.blit(text_gold, text_gold_rect)

    # update the display
    pygame.display.flip()

    if p.current_health == 0:
        running = False

time.sleep(0.25)

if won:
    print("YOU WON")
else:
    print("YOU LOST")

# quit
pygame.quit()
