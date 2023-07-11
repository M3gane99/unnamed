import sys

import pygame.transform
import main_systems as ms

# Zdarzenia ogólne gry
class GameEvent:
    def __init__(self):
        self.font = ms.FONT
        self.font_small = ms.FONT_SMALL
        self.clicked = False # Sprawdza czy nacisnelismy przycisk myszy
        self.menu = True # Sprawdza czy jest odpalone menu
        self.play_btn_color = ms.menu_btns # Kolor przycisku (potrzebne zeby zmienic na kolor hover)
        self.exit_btn_color = ms.menu_btns

    # Wyświtla menu jeżeli zmienna menu jest równa True
    def game_menu(self,surface,info_text=""):
        if self.menu:
            surface.fill(ms.menu_bg) # Tło

            menu_txt = self.font_small.render("Unnamed - Menu", True, ms.silver)
            menu_txt_rect = menu_txt.get_rect()
            menu_txt_rect.centerx = (ms.WIDTH//2)
            menu_txt_rect.centery = 100

            surface.blit(menu_txt, menu_txt_rect)
            if info_text:
                info_txt = self.font_small.render(info_text, True, ms.silver)
                info_txt_rect = info_txt.get_rect()
                info_txt_rect.centerx = (ms.WIDTH // 2)
                info_txt_rect.centery = 200
                surface.blit(info_txt, info_txt_rect)

            play_txt = self.font_small.render("Play / Continue", True, ms.silver)
            exit_txt = self.font_small.render("Quit", True, ms.silver)
            play_txt_rect = play_txt.get_rect()
            exit_txt_rect = exit_txt.get_rect()

            play_txt_rect.centerx = (ms.WIDTH//2)
            exit_txt_rect.centerx = (ms.WIDTH//2)
            play_txt_rect.centery = (ms.HEIGHT//2)-75
            exit_txt_rect.centery = (ms.HEIGHT//2)+25

            m_x, m_y = pygame.mouse.get_pos()
            play_btn = pygame.Rect((ms.WIDTH//2)-125,(ms.HEIGHT//2)-100,250,50)
            exit_btn = pygame.Rect((ms.WIDTH//2)-100,(ms.HEIGHT//2),200,50)

            if play_btn.collidepoint((m_x,m_y)):
                self.play_btn_color = ms.menu_btns_hover
                if self.clicked:
                    self.menu = False
                    return False
            if exit_btn.collidepoint((m_x,m_y)):
                self.exit_btn_color = ms.menu_btns_hover
                if self.clicked:
                    pygame.quit()
                    sys.exit()
            pygame.draw.rect(surface,self.play_btn_color,play_btn)
            pygame.draw.rect(surface,self.exit_btn_color,exit_btn)
            surface.blit(play_txt, play_txt_rect)
            surface.blit(exit_txt, exit_txt_rect)

            #Reset koloru i klikniecia po narysowaniu
            self.play_btn_color = ms.menu_btns
            self.exit_btn_color = ms.menu_btns
            self.clicked = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        self.menu = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicked = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            return True

        return False

    # Puszcza muzykę
    def bgm(self):
        if not pygame.mixer.Channel(3).get_busy():
            pygame.mixer.Channel(3).play(ms.MUSIC_LIST[0])

    # Pokazuje ilość złota na ekranie
    def show_gold(self,surface,gold_amount):
        text = self.font.render(str(gold_amount), True, ms.gold)
        text_rect = text.get_rect()
        if gold_amount < 10:
            text_rect.x = ms.WIDTH-64   # Pozycja ilosci zlota
        elif gold_amount < 100:
            text_rect.x = ms.WIDTH - 86
        else:
            text_rect.x = ms.WIDTH - 108
        text_rect.top = 20

        surface.blit(text,text_rect)
        surface.blit(pygame.transform.scale(ms.GOLD_3,(32,32)),[ms.WIDTH-40, 15])