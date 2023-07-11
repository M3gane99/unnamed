import pygame,os

pygame.init()

SCREEN_SIZE = WIDTH, HEIGHT = 1280, 720 # WIDTH,HEIGHT okna
screen = pygame.display.set_mode(SCREEN_SIZE)

HERO_SIZE = (80,80) # WIDTH,HEIGHT postaci gracza
GRASS_SIZE = (240,80) # WIDTH,HEIGHT pojedynczej platformy z trawy
SLAB_SIZE = (80,40) # WIDTH,HEIGHT pojedynczej platformy z drewna

WORM_SIZE = (64,32) # WIDTH,HEIGHT przeciwnika(Robaka)
MUSHROOM_SIZE = (64,64) # WIDTH,HEIGHT przeciwnika(Grzyba)

# Kolory rgb
gold = (70, 60, 2)
silver = (192,192,192)
menu_bg = (35, 47, 52)
menu_btns = (74, 101, 122)
menu_btns_hover = (52, 73, 85)

# Ściezka do assetów
path = os.path.join(os.curdir, 'assets')
files = sorted(os.listdir(path))

# Usuwam backgroundy z listy
files.remove('BG0.png')
files.remove('BG1.png')
files.remove('BG2.png')
files.remove('BG3.png')

# Tło gry
BACKGROUND = pygame.image.load(os.path.join(path, 'BG0.png')).convert()
BACKGROUND = pygame.transform.scale(BACKGROUND,SCREEN_SIZE)

# Przypisywanie plików do zmiennych globalnych
for file in files:
    image_name = file[:-4].upper()
    globals()[image_name] = pygame.image.load(os.path.join(path, file)).convert_alpha(BACKGROUND)

# Czcionki
FONT = pygame.font.Font('manaspc.ttf', 32)
FONT_SMALL = pygame.font.Font('manaspc.ttf', 24)

# Ustawianie poziomu glosnosci gry
pygame.mixer.Channel(0).set_volume(.3)  # Swing / Gold pickup
pygame.mixer.Channel(1).set_volume(.3)  # Przeciwnicy
pygame.mixer.Channel(2).set_volume(.3)  # Jump / Life / Health
pygame.mixer.Channel(3).set_volume(.13)  # Muzyka

###Gracz

# Muzyka w tle
MUSIC_LIST = [pygame.mixer.Sound('sfx/bgm_by_Muncheybobo_OpenGameArt.mp3')]

# Dźwięki uderzenia mieczem
SWING_LIST = [pygame.mixer.Sound('sfx/swing_1.wav'), pygame.mixer.Sound('sfx/swing_2.wav'),
                   pygame.mixer.Sound('sfx/swing_3.wav')]
# Dzwieki podniesienia złota
GOLD_PICKUP = [pygame.mixer.Sound('sfx/gold.wav')]
# Dzwiek podniesienia zycia
LIFE_PICKUP = [pygame.mixer.Sound("sfx/life.wav")]
# Dzwiek podniesienia zdrowia
HEALTH_PICKUP = [pygame.mixer.Sound("sfx/health.wav")]

# Dzwieki skoku
JUMP_LIST = [pygame.mixer.Sound("sfx/jump.wav")]


# Animacje Idle
HERO_IDLE_LIST_R = [HERO_IDLE_0_R, HERO_IDLE_1_R, HERO_IDLE_2_R, HERO_IDLE_3_R,]
HERO_IDLE_LIST_L = [HERO_IDLE_0_L, HERO_IDLE_1_L, HERO_IDLE_2_L, HERO_IDLE_3_L,]

# Animacje biegu
HERO_RUN_LIST_R = [HERO_RUN_0_R, HERO_RUN_1_R, HERO_RUN_2_R, HERO_RUN_3_R, HERO_RUN_4_R, HERO_RUN_5_R]
HERO_RUN_LIST_L = [HERO_RUN_0_L, HERO_RUN_1_L, HERO_RUN_2_L, HERO_RUN_3_L, HERO_RUN_4_L, HERO_RUN_5_L]

# Animacje popychania
HERO_PUSH_LIST_R = [HERO_PUSH_0_R, HERO_PUSH_1_R, HERO_PUSH_2_R, HERO_PUSH_3_R, HERO_PUSH_4_R, HERO_PUSH_5_R]
HERO_PUSH_LIST_L = [HERO_PUSH_0_L, HERO_PUSH_1_L, HERO_PUSH_2_L, HERO_PUSH_3_L, HERO_PUSH_4_L, HERO_PUSH_5_L]

# Animacje spadania
HERO_FALL_LIST_R = [HERO_FALL_0_R, HERO_FALL_1_R, HERO_FALL_2_R]
HERO_FALL_LIST_L = [HERO_FALL_0_L, HERO_FALL_1_L, HERO_FALL_2_L]

# Animacje skakania
HERO_JUMP_LIST_R = [HERO_JUMP_0_R, HERO_JUMP_1_R, HERO_JUMP_2_R]
HERO_JUMP_LIST_L = [HERO_JUMP_0_L, HERO_JUMP_1_L, HERO_JUMP_2_L]

# Animacje uderzenia mieczem gracza
HERO_SLASHING_LIST_R = [HERO_SLASH_0_R, HERO_SLASH_1_R, HERO_SLASH_2_R, HERO_SLASH_3_R]
HERO_SLASHING_LIST_L = [HERO_SLASH_0_L, HERO_SLASH_1_L, HERO_SLASH_2_L, HERO_SLASH_3_L]

# Animacje uderzenia miecza
HERO_SLASH_LIST_R = [SLASH_0_R, SLASH_1_R, SLASH_2_R, SLASH_3_R]
HERO_SLASH_LIST_L = [SLASH_0_L, SLASH_1_L, SLASH_2_L, SLASH_3_L]


###Tilesy

GRASS_NORMAL_LIST = [GRASS_NORMAL_S, GRASS_NORMAL_L, GRASS_NORMAL_C, GRASS_NORMAL_R]
WOODSLAB_LIST = [WOODSLAB_L, WOODSLAB_C, WOODSLAB_R]


###Przeciwnicy

# Animacje ruchu Grzyba
MUSHROOM_MOVE_LIST_R = [MUSHROOM_0_R, MUSHROOM_1_R, MUSHROOM_2_R, MUSHROOM_3_R,
                        MUSHROOM_4_R, MUSHROOM_5_R, MUSHROOM_6_R, MUSHROOM_7_R]
MUSHROOM_MOVE_LIST_L = [MUSHROOM_0_L, MUSHROOM_1_L, MUSHROOM_2_L, MUSHROOM_3_L,
                        MUSHROOM_4_L, MUSHROOM_5_L, MUSHROOM_6_L, MUSHROOM_7_L]

# Dzwieki smierci Grzyba
MUSHROOM_DEATH_LIST = [pygame.mixer.Sound('sfx/mushroom_death.wav')]

# Animacje otrzymania obrazen Grzyba
MUSHROOM_HIT_LIST_R = [MUSHROOM_HIT_0_R, MUSHROOM_HIT_1_R, MUSHROOM_HIT_2_R]
MUSHROOM_HIT_LIST_L = [MUSHROOM_HIT_0_L, MUSHROOM_HIT_1_L, MUSHROOM_HIT_2_L]

# Animacje śmierci Grzyba
MUSHROOM_DEATH_LIST_R = [MUSHROOM_DEATH_0_R, MUSHROOM_DEATH_1_R, MUSHROOM_DEATH_2_R,
                         MUSHROOM_DEATH_3_R, MUSHROOM_DEATH_4_R, MUSHROOM_DEATH_5_R]
MUSHROOM_DEATH_LIST_L = [MUSHROOM_DEATH_0_L, MUSHROOM_DEATH_1_L, MUSHROOM_DEATH_2_L,
                         MUSHROOM_DEATH_3_L, MUSHROOM_DEATH_4_L, MUSHROOM_DEATH_5_L]

# Animacje ruchu Robaka
WORM_MOVE_LIST_R = [WORM_0_R, WORM_1_R, WORM_2_R, WORM_3_R, WORM_4_R, WORM_5_R]
WORM_MOVE_LIST_L = [WORM_0_L, WORM_1_L, WORM_2_L, WORM_3_L, WORM_4_L, WORM_5_L]

# Dzwieki smierci Robaka
WORM_DEATH_LIST = [pygame.mixer.Sound('sfx/worm_death.wav')]

# Animacje otrzymania obrazen Robaka
WORM_HIT_LIST_R = [WORM_HIT_0_R, WORM_HIT_1_R, WORM_HIT_2_R]
WORM_HIT_LIST_L = [WORM_HIT_0_L, WORM_HIT_1_L, WORM_HIT_2_L]

# Animacje śmierci Robaka
WORM_DEATH_LIST_R = [WORM_DEATH_0_R, WORM_DEATH_1_R, WORM_DEATH_2_R, WORM_DEATH_3_R,
                     WORM_DEATH_4_R, WORM_DEATH_5_R]
WORM_DEATH_LIST_L = [WORM_DEATH_0_L, WORM_DEATH_1_L, WORM_DEATH_2_L, WORM_DEATH_3_L,
                     WORM_DEATH_4_L, WORM_DEATH_5_L]