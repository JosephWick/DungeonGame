import pygame

from Wall import Wall
from HealthPotion import HealthPotion
from GoldCoin import GoldCoin
from ArrowBox import ArrowBox
from Enemy import Enemy
from ObjectTopDown import ObjectTopDown


class Map():
    def __init__(self, map_dim, screen_dim, image_dict):
        """
        image_dict should have: "wall", "coin", "arrow", "health", "enemy"
        """

        self.map_dim = map_dim
        self.screen_dim = screen_dim

        self.wall_img = image_dict["wall"]
        self.health_img = image_dict["health"]
        self.coin_img = image_dict["coin"]
        self.arrow_img = image_dict["arrow"]
        self.enemy_img = image_dict["enemy"]
        self.portal_img = image_dict["portal"]

        self.x_shift = self.map_dim[0]/2 - self.screen_dim[0]/2
        self.y_shift = self.map_dim[1]/2 - self.screen_dim[1]/2

    def make_map(self, file):
        # spawn a bunch of walls at specified positions
        #data = np.loadtxt(wallsfile, delimiter=",", skiprows=1)

        walls_group = pygame.sprite.Group()
        items_group = pygame.sprite.Group()
        enemies_group = pygame.sprite.Group()
        portals_group = pygame.sprite.Group()

        with open(file, "r") as f:
            for i, line in enumerate(f):
                for j, c in enumerate(line):
                    loc = (50*j - self.x_shift, 50*i - self.y_shift)
                    if c=="w":
                        new_wall = Wall(self.wall_img, loc)
                        walls_group.add(new_wall)
                    elif c=="h":
                        new_health = HealthPotion(self.health_img, loc)
                        items_group.add(new_health)
                    elif c=="c":
                        new_coin = GoldCoin(self.coin_img, loc)
                        items_group.add(new_coin)
                    elif c=="a":
                        new_arrow = ArrowBox(self.arrow_img, loc)
                        items_group.add(new_arrow)
                    elif c=="e":
                        new_enemy = Enemy(self.enemy_img, loc)
                        enemies_group.add(new_enemy)
                    elif c=="p":
                        new_portal = ObjectTopDown([self.portal_img], -1)
                        new_portal.rect.center = loc
                        portals_group.add(new_portal)

        return walls_group, items_group, enemies_group, portals_group
