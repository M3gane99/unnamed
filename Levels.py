import pygame
import main_systems as ms


#Ogólna klasa wroga
class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_image, image_list_left, image_list_right, image_list_dead_left,
                 image_list_dead_right, health, image_list_hit_left, image_list_hit_right, name, movement_x = 0, movement_y = 0):
        super().__init__()
        self.image = start_image
        self.rect = self.image.get_rect()
        self.image_list_left = image_list_left
        self.image_list_right = image_list_right
        self.image_list_dead_left = image_list_dead_left
        self.image_list_dead_right = image_list_dead_right
        self.image_list_hit_left = image_list_hit_left
        self.image_list_hit_right = image_list_hit_right
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.health = health
        self.rotate_left = False
        self.count = 0  # -1 gdy skończy się animacja śmierci
        self.death_anim = False # Żeby wiedzieć, że dana animacja jest animacją śmierci
        self.hit_anim = False # To samo,tylko dla animacji otrzymania obrazen
        self.dead = False # Potrzebne, ponieważ self.kill nie działa na grupie... lepszego rozwiązania na razie nie ma
        self.name = name # Jak się nazywa potwór, żeby odtworzyc odpowiedni dzwiek jego smierci

    def update(self):
        if not self.health and self.count == -1:
            self.dead = True

        # Ruch przeciwnika
        self.rect.x += self.movement_x

        if self.movement_x > 0 and self.rotate_left:
            self.rotate_left = False
        if self.movement_x < 0 and not self.rotate_left:
            self.rotate_left = True

        # Animacje
        if self.health > 0 and not self.hit_anim:
            if self.movement_x > 0:
                self._move(self.image_list_right,len(self.image_list_right))
            if self.movement_x < 0:
                self._move(self.image_list_left,len(self.image_list_left))
        elif self.health <= 0:
            self.movement_x = 0
            self.movement_y = 0
            self.death_anim = True

            if self.rotate_left:
                self._move(self.image_list_dead_left,len(self.image_list_dead_left))
            if not self.rotate_left:
                self._move(self.image_list_dead_right,len(self.image_list_dead_right))
        elif self.hit_anim:
            if self.movement_x > 0:
                self._move(self.image_list_hit_right,len(self.image_list_hit_right))
            if self.movement_x < 0:
                self._move(self.image_list_hit_left,len(self.image_list_hit_left))

    # Zmiana grafik podczas animacji
    def _move(self, image_list, image_list_len):
        if image_list_len == 6: #Animacje robaka / animacje śmierci
            if self.count < 3:
                self.image = image_list[0]
            elif self.count < 6:
                self.image = image_list[1]
            elif self.count < 9:
                self.image = image_list[2]
            elif self.count < 12:
                self.image = image_list[3]
            elif self.count < 15:
                self.image = image_list[4]
            elif self.count < 18:
                self.image = image_list[5]

            if self.count < 18:
                self.count += 1
            else:
                if self.death_anim:
                    self.count = -1
                else:
                    self.count = 0

        elif image_list_len == 8:  # Animacje grzyba
            if self.count < 3:
                self.image = image_list[0]
            elif self.count < 6:
                self.image = image_list[1]
            elif self.count < 9:
                self.image = image_list[2]
            elif self.count < 12:
                self.image = image_list[3]
            elif self.count < 15:
                self.image = image_list[4]
            elif self.count < 18:
                self.image = image_list[5]
            elif self.count < 21:
                self.image = image_list[6]
            elif self.count < 24:
                self.image = image_list[7]

            if self.count < 24:
                self.count += 1
            else:
                self.count = 0

        elif image_list_len == 3:  # Animacja otrzymania obrazen
            if self.count < 3:
                self.image = image_list[0]
            elif self.count < 6:
                self.image = image_list[1]
            elif self.count < 9:
                self.image = image_list[2]
            if self.count < 9:
                self.count += 1
            else:
                self.count = 0
                self.hit_anim = False

# Przeciwnik (Robak)
class Worm(Enemy):
    def __init__(self, start_image, image_list_left, image_list_right, image_list_dead_left,
                 image_list_dead_right,level, health, image_list_hit_left, image_list_hit_right, x1, x2, y,size, name, movement_x=0, movement_y=0):
        super().__init__(start_image,image_list_left,image_list_right,image_list_dead_left,
                       image_list_dead_right, health, image_list_hit_left, image_list_hit_right, name, movement_x, movement_y)
        self.rect = pygame.transform.scale(self.image,size).get_rect()
        self.level = level
        self.x1 = x1    #Pozycja startowa ścieżki
        self.x2 = x2    #Pozycja do której przeciwnik dojdzie
        self.rect.left = x1
        self.rect.bottom = y
        self.size = size

    def update(self):
        super().update()
        pos_x = self.rect.left - self.level.world_shift_x
        if (pos_x < self.x1 or pos_x + self.rect.width > self.x2):
            self.movement_x *= -1

    def draw(self,surface):
        surface.blit(pygame.transform.scale(self.image,self.size),self.rect)

# Przeciwnik (Grzyb)
class Mushroom(Enemy):
    def __init__(self, start_image, image_list_left, image_list_right, image_list_dead_left,
                 image_list_dead_right,level, health, image_list_hit_left, image_list_hit_right, x1, x2, y, size, name, movement_x=0, movement_y=0):
        super().__init__(start_image,image_list_left,image_list_right,image_list_dead_left,
                       image_list_dead_right, health, image_list_hit_left, image_list_hit_right, name, movement_x, movement_y)
        self.rect = pygame.transform.scale(self.image,size).get_rect()
        self.level = level
        self.x1 = x1    #Pozycja startowa ścieżki
        self.x2 = x2    #Pozycja do której przeciwnik dojdzie
        self.rect.left = x1
        self.rect.bottom = y
        self.size = size

    def update(self):
        super().update()
        pos_x = self.rect.left - self.level.world_shift_x
        if (pos_x < self.x1 or pos_x + self.rect.width > self.x2):
            self.movement_x *= -1

    def draw(self,surface):
        surface.blit(pygame.transform.scale(self.image,self.size),self.rect)

# Klasa platformy
class Platform(pygame.sprite.Sprite):
    def __init__(self, image_list, width, height, pos_x, pos_y, is_starting = False):
        super().__init__()
        self.image_list = image_list
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.is_starting = True if is_starting else False # Ustala czy ta platforma jest startowa

    # Rysuje platformy w zaleznosci od ich typu.
    # Te z listą długości 4 to większe, z grafiką trawy
    # Te z listą długości 3 są z grafiką drewna
    def draw(self, surface):
        if len(self.image_list) == 4:
            if self.width == (240):
                surface.blit(pygame.transform.scale(self.image_list[0],ms.GRASS_SIZE), self.rect)
            else:
                surface.blit(pygame.transform.scale(self.image_list[1],ms.GRASS_SIZE), self.rect)
                for i in range(240, self.width - 240, 240):
                    surface.blit(pygame.transform.scale(self.image_list[2], ms.GRASS_SIZE), [self.rect.x + i, self.rect.y])
                surface.blit(pygame.transform.scale(self.image_list[3], ms.GRASS_SIZE), [self.rect.x + self.width - 240, self.rect.y])
        elif len(self.image_list) == 3:
            if self.width == (240):
                surface.blit(pygame.transform.scale(self.image_list[0],ms.SLAB_SIZE), self.rect)
                surface.blit(pygame.transform.scale(self.image_list[1],ms.SLAB_SIZE), [self.rect.x + 80, self.rect.y])
                surface.blit(pygame.transform.scale(self.image_list[2],ms.SLAB_SIZE), [self.rect.x + 160, self.rect.y])
            else:
                surface.blit(pygame.transform.scale(self.image_list[0],ms.SLAB_SIZE), self.rect)
                for i in range(80, self.width - 80, 80):
                    surface.blit(pygame.transform.scale(self.image_list[1], ms.SLAB_SIZE), [self.rect.x + i, self.rect.y])
                surface.blit(pygame.transform.scale(self.image_list[2], ms.SLAB_SIZE), [self.rect.x + self.width - 80, self.rect.y])

# Główna klasa poziomu
class Level:
    def __init__(self, player):
        self.player = player
        self.set_of_platforms = set()
        self.set_of_items = pygame.sprite.Group()
        self.set_of_misc = pygame.sprite.Group()
        self.set_of_enemies = set()
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.starting_x = 0
        self.starting_y = 0
        self.won = False    # Kiedy gracz ukonczy poziom
        self.gold_in_level = 0

    def update(self):
        # Updatuje przeciwników / w razie ich śmierci usuwa ich z planszy
        for e in self.set_of_enemies:
            e.update()
            if e.dead:
                self.set_of_enemies.remove(e)
                break

        # Przesunięcie świata (kamery)
        if self.player.rect.right >= ms.WIDTH-400:
            diff = self.player.rect.right - (ms.WIDTH-400)
            self.player.rect.right = ms.WIDTH-400
            self._shift_world_x(-diff)

        if self.player.rect.left <= 400:
            diff = 400 - self.player.rect.left
            self.player.rect.left = 400
            self._shift_world_x(diff)

        if self.player.rect.top <= 200:
            diff = 200 - self.player.rect.top
            self.player.rect.top = 200
            self._shift_world_y(diff)

        if self.player.rect.bottom >=  ms.HEIGHT-200:
            diff = self.player.rect.bottom - (ms.HEIGHT-200)
            self.player.rect.bottom = (ms.HEIGHT-200)
            self._shift_world_y(-diff)

    # Rysowanie poziomu
    def draw(self, surface):
        # Rysowanie platform / przeciwników / przedmiotów / obiektów
        for p in self.set_of_platforms:
            p.draw(surface)
        for e in self.set_of_enemies:
            e.draw(surface)
        self.set_of_items.draw(surface)
        self.set_of_misc.draw(surface)

        # HUD (życia) - Ile masz żyć do końca gry
        for i in range(self.player.lifes - 1):
           surface.blit(pygame.transform.scale(ms.LIFE,(64,64)), [20 + 60 * i, 15])

        # HUD (zdrowie) - Ile ataków przeciwnika przetrwasz
        for i in range(self.player.health):
           surface.blit(pygame.transform.scale(ms.HEART,(32,32)), [20 + 45 * i, 80])

    # Przesunięcie świata kiedy zmieniamy naszą pozycję
    def _shift_world_x(self, shift_x):
        self.world_shift_x += shift_x

        for p in self.set_of_platforms:
            p.rect.x += shift_x

        for item in self.set_of_items:
            item.rect.x += shift_x

        for misc in self.set_of_misc:
            misc.rect.x += shift_x

        for e in self.set_of_enemies:
            e.rect.x += shift_x

    # Przesunięcie świata kiedy zmieniamy naszą pozycję
    def _shift_world_y(self, shift_y):
        self.world_shift_y += shift_y

        for p in self.set_of_platforms:
            p.rect.y += shift_y

        for item in self.set_of_items:
            item.rect.y += shift_y

        for misc in self.set_of_misc:
            misc.rect.y += shift_y

        for e in self.set_of_enemies:
            e.rect.y += shift_y

# Klasa pierwszego poziomu
class Level1(Level):
    def __init__(self, player = None):
        super().__init__(player)
        # Inicjalizacja obiektów poziomu
        self._create_platforms()
        self._create_itmes()
        self._create_miscs()
        self._create_enemies()

    # Tworzenie platform na mapie
    def _create_platforms(self):
        # Ustawiam pozycje startowe (w razie śmierci tutaj postać zostanie przeniesiona)
        self.starting_x = 360
        self.starting_y = 380

        # Tworzenie platform z trawą
        grass_platforms = [[2*240,80,240,400],[6*240, 80, 480 , 600],[3*240, 80, 1920, 680],
                           [240,80,4000,250],[240,80,3800,0],[240,80,4200,-200],
                           [6*240,80,4600,-380],[10*240,80,5940,-200],[240,80,8700,-750],
                           [6*240,80,9200,-1000],[6*240,80,10640,-800],[240,80,12340,-1000],[10*240,80,12740,-1200]]

        # Wpisanie platform do listy (trawiaste)
        for ws in grass_platforms:
            if ws[2] == 240 and ws[3] == 400: # Ustawia pierwszą platformę jako startową(do respawnu)
                p = Platform(ms.GRASS_NORMAL_LIST, *ws,True)
                self.set_of_platforms.add(p)
                continue
            p = Platform(ms.GRASS_NORMAL_LIST, *ws)
            self.set_of_platforms.add(p)

        # Wpisanie platform do listy (drewniane)
        woodenslab_platforms = [[240,40,2640,560], [2*240,40,3200,450], [240,40,6100,-580], [240,40,6600,-300], [240,40,7200,-480],
                                [2*240,40,8500,-350],[4*240,40,8900,-500],[240,40,9100,-100],[2*240,40,15400,-1380]]
        for ws in woodenslab_platforms:
            p = Platform(ms.WOODSLAB_LIST,*ws)
            self.set_of_platforms.add(p)

    # Przedmioty do podnoszenia
    def _create_itmes(self):
        health_1 = Item(pygame.transform.scale(ms.HEART,(48,48)), 'health', 3440, 402)
        coin_1 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 640, 600-32)
        coin_2 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 700, 600-32)
        coin_3 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 760, 600-32)
        coin_4 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 820, 600-32)
        coin_5 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 2100, 680-32)
        coin_6 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 2160, 600-32)
        coin_7 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 2220, 600-32)
        coin_8 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 2280, 400-32)
        coin_9 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 2220, 400-32)
        coin_10 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 4080, 250-32)
        coin_11 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 4700, -380-32)
        coin_12 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 4900, -380-32)
        coin_13 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 5400, -700-32)
        coin_14 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 5500, -700-32)
        coin_15 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 5900, -380-32)
        coin_16 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 6220, -580-32)
        coin_17 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 6720, -300-32)
        life_1 = Item(pygame.transform.scale(ms.LIFE, (48, 48)), 'life', 6800, -300-32)
        coin_18 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 7600, -580-32)
        coin_19 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 7800, -480-32)
        coin_20 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 8000, -380-32)
        coin_21 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 8200, -200-32)
        coin_22 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 9140, -100-32)
        coin_23 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 9300, -100-32)
        health_2 = Item(pygame.transform.scale(ms.HEART,(48,48)), 'health', 9220, -100-32)
        coin_24 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 9250, -1050-32)
        coin_25 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 9600, -1250-32)
        coin_26 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 9900, -1150-32)
        coin_27 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 10400, -1000-32)
        coin_28 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 9600, -1000-32)
        coin_29 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 10840, -800-32)
        coin_30 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 11040, -800-32)
        coin_31 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 11240, -800-32)
        life_2 = Item(pygame.transform.scale(ms.LIFE, (48, 48)), 'life', 11400, -800-32)
        coin_32 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 11640, -800-32)
        coin_33 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 12400, -1000-32)
        coin_34 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 13400, -1300-32)
        coin_35 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 13800, -1400-32)
        coin_36 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 14200, -1400-32)
        coin_37 = Item(pygame.transform.scale(ms.GOLD_3,(32,32)), 'gold', 14800, -1300-32)
        self.set_of_items.add(health_1,coin_1,coin_2,coin_3,coin_4,coin_5,
                              coin_6,coin_7,coin_8,coin_9,coin_10,
                              coin_11,coin_12,coin_13,coin_14,coin_15,
                              coin_16,coin_17,life_1,coin_18,coin_19,
                              coin_20,coin_21,coin_22,coin_23,health_2,
                              coin_24,coin_25,coin_26,coin_27,coin_28,
                              coin_29,coin_30,coin_31,life_2,coin_32,
                              coin_33,coin_34,coin_35,coin_36,coin_37)
        for object in self.set_of_items:
            if object.name == 'gold':
                self.gold_in_level += 1

    # Obiekty drugoplanowe na mapie(znaki, trawa, ...)
    def _create_miscs(self):
        # Wiadomosci fabularne(';' - separator nowej linii)
        sign_1 = Misc(pygame.transform.scale(ms.ARROW_R,(80,80)),False,1080,600, text="- Where am I? I don't remember anything... and why do I look like a ghost?!;"
                                                                                      "Should I follow along this path?")
        sign_2 = Misc(pygame.transform.scale(ms.SIGN,(80,80)),False,4700,-380, text="'You should watch for those big bois...' - Who wrote that!?;"
                                                                                    "What is this monster? Actually what were does from earlier...")
        sign_3 = Misc(pygame.transform.scale(ms.SIGN,(80,80)),False,9300,-1000, text="'You are closer and closer, just a few more monster to slay and;"
                                                                                     "you will be granted ascension' - Oh, I remember now. I died in an accident...")
        sign_4 = Misc(pygame.transform.scale(ms.ARROW_R,(80,80)),False,12500,-1000, text="'Feeling defeated yet? ... No? Well, you should be.;"
                                                                                         "This is your last trial, slay the last monsters and gain your reward';"
                                                                                         "- This shouldn't be that hard... I will be free... at last!")
        self.set_of_misc.add(sign_1,sign_2,sign_3,sign_4)

        # Trawa dla ozdoby
        grass_1 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,600,600)
        grass_2 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,720,600)
        grass_3 = Misc(pygame.transform.scale(ms.GRASS, (48, 24)), False, 1200, 600)
        grass_4 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,1560,600)
        grass_5 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,2040,680)
        grass_6 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,4060,250)
        grass_7 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,3920,0)
        grass_8 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,4800,-380)
        grass_9 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,4860,-380)
        grass_10 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,5660,-380)
        grass_11 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,5800,-380)
        grass_12 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,7800,-200)
        grass_13 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,8000,-200)
        grass_14 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,8250,-200)
        grass_15 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,8800,-750)
        grass_16 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,8900,-750)
        grass_17 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,9280,-1000)
        grass_18 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,9600,-1000)
        grass_19 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,9950,-1000)
        grass_20 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,10150,-1000)
        grass_21 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,12400,-1000)
        grass_22 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,12800,-1200)
        grass_23 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,13500,-1200)
        grass_24 = Misc(pygame.transform.scale(ms.GRASS_DRY,(48,24)),False,13800,-1200)
        grass_25 = Misc(pygame.transform.scale(ms.GRASS,(48,24)),False,14500,-1200)
        self.set_of_misc.add(grass_1,grass_2,grass_3,grass_4,grass_5,
                             grass_6,grass_7,grass_8,grass_9,grass_10,
                             grass_11,grass_12,grass_13,grass_14,grass_15,grass_16,
                             grass_17,grass_18,grass_19,grass_20,grass_21,
                             grass_22,grass_23,grass_24,grass_25)

        # Kamienie dla ozdoby / jako przeszkoda
        stone_1 = Misc(pygame.transform.scale(ms.STONE, (80, 80)), True, 1800, 600)
        stone_2 = Misc(pygame.transform.scale(ms.STONE, (80, 80)), True, 2500, 680)
        stone_3 = Misc(pygame.transform.scale(ms.STONE, (80, 80)), True, 5000, -380)
        stone_4 = Misc(pygame.transform.scale(ms.STONE, (80, 80)), True, 9460, -1000)
        stone_5 = Misc(pygame.transform.scale(ms.STONE, (80, 80)), True, 9800, -1000)
        stone_6 = Misc(pygame.transform.scale(ms.STONE, (80, 80)), True, 13100, -1200)
        self.set_of_misc.add(stone_1,stone_2,stone_3,stone_4,stone_5,stone_6)

        # Drzwi do ukończenia poziomu
        winning_door = Misc(pygame.transform.scale(ms.DOOR, (120, 120)), False, 15800, -1380,winning_door=True)
        self.set_of_misc.add(winning_door)

        # Pułapki
        spike_1 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,2420,680,trap=True)

        spike_2 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,6040,-200,trap=True)
        spike_3 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,6140,-200,trap=True)
        spike_4 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,6240,-200,trap=True)
        spike_5 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,6340,-200,trap=True)
        spike_6 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,6440,-200,trap=True)
        spike_7 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,6540,-200,trap=True)
        spike_8 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,6640,-200,trap=True)
        spike_9 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,6740,-200,trap=True)
        spike_10 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,6840,-200,trap=True)
        spike_11 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,6940,-200,trap=True)
        spike_12 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,7040,-200,trap=True)
        spike_13 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,7140,-200,trap=True)
        spike_14 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,7240,-200,trap=True)
        spike_15 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,7340,-200,trap=True)
        spike_16 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,7440,-200,trap=True)
        spike_17 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,10040,-1000,trap=True)
        spike_18 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,10740,-800,trap=True)
        spike_19 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,10940,-800,trap=True)
        spike_20 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,11140,-800,trap=True)
        spike_21 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,11540,-800,trap=True)
        spike_22 = Misc(pygame.transform.scale(ms.SPIKES_TRAP,(64,64)),False,11740,-800,trap=True)

        self.set_of_misc.add(spike_1,spike_2,spike_3,spike_4,spike_5,
                             spike_6,spike_7,spike_8,spike_9,spike_10,
                             spike_11,spike_12,spike_13,spike_14,spike_15,
                             spike_16,spike_17,spike_18,spike_19,
                             spike_20,spike_21,spike_22)

    # Przeciwnicy na mapie
    def _create_enemies(self):
        worm_1 = Worm(ms.WORM_0_R, ms.WORM_MOVE_LIST_L, ms.WORM_MOVE_LIST_R,
                      ms.WORM_DEATH_LIST_L, ms.WORM_DEATH_LIST_R, self, 1, ms.WORM_HIT_LIST_L, ms.WORM_HIT_LIST_R, 800,1200,600,ms.WORM_SIZE,"Worm",3)
        worm_2 = Worm(ms.WORM_0_R, ms.WORM_MOVE_LIST_L, ms.WORM_MOVE_LIST_R,
                      ms.WORM_DEATH_LIST_L, ms.WORM_DEATH_LIST_R, self, 1, ms.WORM_HIT_LIST_L, ms.WORM_HIT_LIST_R, 1200, 1600, 600,ms.WORM_SIZE,"Worm",3)
        worm_3 = Worm(ms.WORM_0_R, ms.WORM_MOVE_LIST_L, ms.WORM_MOVE_LIST_R,
                      ms.WORM_DEATH_LIST_L, ms.WORM_DEATH_LIST_R, self, 1, ms.WORM_HIT_LIST_L, ms.WORM_HIT_LIST_R, 6100, 6340, -580,ms.WORM_SIZE,"Worm",3)
        worm_4 = Worm(ms.WORM_0_R, ms.WORM_MOVE_LIST_L, ms.WORM_MOVE_LIST_R,
                      ms.WORM_DEATH_LIST_L, ms.WORM_DEATH_LIST_R, self, 1, ms.WORM_HIT_LIST_L, ms.WORM_HIT_LIST_R, 7200, 7440, -480,ms.WORM_SIZE,"Worm", 3)
        worm_5 = Worm(ms.WORM_0_R, ms.WORM_MOVE_LIST_L, ms.WORM_MOVE_LIST_R,
                      ms.WORM_DEATH_LIST_L, ms.WORM_DEATH_LIST_R, self, 1, ms.WORM_HIT_LIST_L, ms.WORM_HIT_LIST_R, 9200, 9860, -500,ms.WORM_SIZE,"Worm", 3)
        worm_6 = Worm(ms.WORM_0_R, ms.WORM_MOVE_LIST_L, ms.WORM_MOVE_LIST_R,
                      ms.WORM_DEATH_LIST_L, ms.WORM_DEATH_LIST_R, self, 1, ms.WORM_HIT_LIST_L, ms.WORM_HIT_LIST_R, 8900, 9860, -500,ms.WORM_SIZE,"Worm", 3)
        worm_7 = Worm(ms.WORM_0_R, ms.WORM_MOVE_LIST_L, ms.WORM_MOVE_LIST_R,
                      ms.WORM_DEATH_LIST_L, ms.WORM_DEATH_LIST_R, self, 1, ms.WORM_HIT_LIST_L, ms.WORM_HIT_LIST_R, 11180, 11540, -800,ms.WORM_SIZE,"Worm", 3)
        worm_8 = Worm(ms.WORM_0_R, ms.WORM_MOVE_LIST_L, ms.WORM_MOVE_LIST_R,
                      ms.WORM_DEATH_LIST_L, ms.WORM_DEATH_LIST_R, self, 8, ms.WORM_HIT_LIST_L, ms.WORM_HIT_LIST_R, 13140, 15140, -1200,(256,128),"Worm", 5)
        worm_9 = Worm(ms.WORM_0_R, ms.WORM_MOVE_LIST_L, ms.WORM_MOVE_LIST_R,
                      ms.WORM_DEATH_LIST_L, ms.WORM_DEATH_LIST_R, self, 8, ms.WORM_HIT_LIST_L, ms.WORM_HIT_LIST_R, 14140, 15140, -1200,(256,128),"Worm", 5)

        self.set_of_enemies.add(worm_1)
        self.set_of_enemies.add(worm_2)
        self.set_of_enemies.add(worm_3)
        self.set_of_enemies.add(worm_4)
        self.set_of_enemies.add(worm_5)
        self.set_of_enemies.add(worm_6)
        self.set_of_enemies.add(worm_7)
        self.set_of_enemies.add(worm_8)
        self.set_of_enemies.add(worm_9)

        shroom_1 = Mushroom(ms.MUSHROOM_0_R, ms.MUSHROOM_MOVE_LIST_L, ms.MUSHROOM_MOVE_LIST_R,
                            ms.MUSHROOM_DEATH_LIST_L, ms.MUSHROOM_DEATH_LIST_R, self, 2, ms.MUSHROOM_HIT_LIST_L, ms.MUSHROOM_HIT_LIST_R, 2640,2880,560,ms.MUSHROOM_SIZE,"Mushroom",2)
        shroom_2 = Mushroom(ms.MUSHROOM_0_R, ms.MUSHROOM_MOVE_LIST_L, ms.MUSHROOM_MOVE_LIST_R,
                            ms.MUSHROOM_DEATH_LIST_L, ms.MUSHROOM_DEATH_LIST_R, self, 5, ms.MUSHROOM_HIT_LIST_L, ms.MUSHROOM_HIT_LIST_R, 5080,5660,-380,(128,128),"Mushroom",3)
        shroom_3 = Mushroom(ms.MUSHROOM_0_R, ms.MUSHROOM_MOVE_LIST_L, ms.MUSHROOM_MOVE_LIST_R,
                            ms.MUSHROOM_DEATH_LIST_L, ms.MUSHROOM_DEATH_LIST_R, self, 2, ms.MUSHROOM_HIT_LIST_L, ms.MUSHROOM_HIT_LIST_R, 6600,6840,-300,ms.MUSHROOM_SIZE,"Mushroom",2)
        shroom_4 = Mushroom(ms.MUSHROOM_0_R, ms.MUSHROOM_MOVE_LIST_L, ms.MUSHROOM_MOVE_LIST_R,
                            ms.MUSHROOM_DEATH_LIST_L, ms.MUSHROOM_DEATH_LIST_R, self, 2, ms.MUSHROOM_HIT_LIST_L, ms.MUSHROOM_HIT_LIST_R, 8700,8940,-750,ms.MUSHROOM_SIZE,"Mushroom",2)
        shroom_5 = Mushroom(ms.MUSHROOM_0_R, ms.MUSHROOM_MOVE_LIST_L, ms.MUSHROOM_MOVE_LIST_R,
                            ms.MUSHROOM_DEATH_LIST_L, ms.MUSHROOM_DEATH_LIST_R, self, 5, ms.MUSHROOM_HIT_LIST_L, ms.MUSHROOM_HIT_LIST_R, 10100,10640,-1000,(128,128),"Mushroom",3)
        self.set_of_enemies.add(shroom_1)
        self.set_of_enemies.add(shroom_2)
        self.set_of_enemies.add(shroom_3)
        self.set_of_enemies.add(shroom_4)
        self.set_of_enemies.add(shroom_5)


# Klasa przedmiotów do podnoszenia
class Item(pygame.sprite.Sprite):
    def __init__(self, image, name, pos_center_x, pos_center_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.name = name # Potrzebna do określania typu przedmiotu
        self.rect.center = [pos_center_x, pos_center_y]
    def kill(self):
        super().kill()


# Klasa obiektów dekoracyjnych / przeszkód
class Misc(pygame.sprite.Sprite):
    def __init__(self, image,collide, pos_bottom_x, pos_bottom_y, text="", trap=False, winning_door=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.collide = collide # Określa czy postać gracza ma kolidować z tym obiektem
        self.rect.center = [pos_bottom_x, pos_bottom_y-self.rect.height/2]
        self.trap = trap # Czy wstawiany obiekt jest pułapką
        self.text = text # Wiadomość tekstowa, jeśli obiekt ma być interaktywny
        self.winning_door = winning_door # Czy dany obiekt kończy grę / poziom
