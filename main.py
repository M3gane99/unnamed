import pygame,os
import main_systems as ms
from Player import Player
from Levels import Level1
from game_events import GameEvent

# Centrowanie okna / inicjalizacja
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# ustawienia ekranu i gry
screen = pygame.display.set_mode(ms.SCREEN_SIZE)
pygame.display.set_caption('Unnamed')
clock = pygame.time.Clock()

#Tworzenie podstawowych obiektów
player = Player(ms.HERO_IDLE_1_R)
player.rect.center = screen.get_rect().center
current_level = Level1(player)
player.level = current_level
g_events = GameEvent()

# Pętla gry
window_open = True
while window_open:
    # Muzyka w tle
    g_events.bgm()

    # Ekran wygranej
    if current_level.won:
        g_events.menu = True
        if g_events.game_menu(screen,info_text="You Won! You've collected " + str(player.gold) + " / " + str(current_level.gold_in_level) + " gold."):
            # Aktualizacja okna
            pygame.display.flip()
            clock.tick(30)
            continue
        else:
            player = Player(ms.HERO_IDLE_1_R)
            player.rect.center = screen.get_rect().center
            current_level = Level1(player)
            player.level = current_level

    # Ekran przegranej
    if player.lifes <= 0:
        g_events.menu = True
        if g_events.game_menu(screen,info_text="You Lost, try again..."):
            # Aktualizacja okna
            pygame.display.flip()
            clock.tick(30)
            continue
        else:
            player = Player(ms.HERO_IDLE_1_R)
            player.rect.center = screen.get_rect().center
            current_level = Level1(player)
            player.level = current_level
    else:
        screen.blit(ms.BACKGROUND, (0, 0))

    # Ekran menu / pauzy
    if g_events.game_menu(screen):
        # Aktualizacja okna
        pygame.display.flip()
        clock.tick(30)
        continue
    if g_events.clicked:    # Po rozpoczeciu / odpauzowaniu gry zeruje akcje gracza (pozycja itp)
        g_events.clicked = False
        player.clear()

    # Pętla zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                g_events.menu = True
        elif event.type == pygame.QUIT:
            window_open = False
        player.get_event(event)

    # Aktualizacja obiektów
    current_level.update()
    player.update()
    current_level.draw(screen)
    player.draw(screen)
    g_events.show_gold(screen,player.gold)

    # Aktualizacja okna
    pygame.display.flip()
    clock.tick(30)

pygame.quit()