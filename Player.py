import pygame, main_systems as ms
import random

# Atak gracza
class Attack(pygame.sprite.Sprite):
    def __init__(self,rect_new):
        self.rect = pygame.Rect(rect_new)
        self._count = 0
        self.image = ms.SLASH_NONE
        self.is_slashing = False # Jeśli true to postać właśnie ciacha mieczem
        self.slashed = False # Zapobiega wielokrotnemu wykryciu przeciwnika podczas ciachania mieczem

    def draw(self,surface):
        surface.blit(pygame.transform.scale(self.image, ms.HERO_SIZE), self.rect)

    # Animacje ataku / zmiana grafik
    def Slash(self, image_list):
        if self._count < 3:
            self.image = image_list[0]
        elif self._count < 6:
            self.image = image_list[1]
        elif self._count < 9:
            self.image = image_list[2]
        elif self._count < 12:
            self.image = image_list[3]

        if self._count < 12:
            self._count += 1
        else:
            self._count = 0
            self.is_slashing = False
            self.slashed = False
            self.image = ms.SLASH_NONE

# Gracz
class Player(pygame.sprite.Sprite):
    def __init__(self, file_image):
        super().__init__()
        self.image = file_image
        self.rect = pygame.transform.scale(self.image,ms.HERO_SIZE).get_rect()
        self.attack = Attack(self.rect)
        self.jump_power = -16

        self.movement_x = 0
        self.movement_y = 0
        self.press_left = False
        self.press_right = False
        self.rotate_left = False
        self._count = 0
        self.level = None
        self.health = 2
        self.lifes = 2
        self.was_hit = False     # Blokuje inputy gracza gdy zostanie on uderzony przez potwora
        self.was_hit_trap = False     # Blokuje inputy gracza gdy wpadnie on w pułapkę
        self.tickCounter = 0    # Liczy ilosc iteracji, aby wykonywac niektóre działania przez określony okres czasu
        self.gold = 0   # Licznik złota
        self.interacted = False # Okresla czy wcisnelismy przycisk interakcji
        self.interactable_text = "" # Ustawia tekst wiadomosci jesli stoimy w odpowiednim miejscu

        # Jeżeli przeciwnik atakował z prawej do lewej to zostaniemy wyrzuceni w lewą stronę (wartość -1)
        # A jeżeli atakował z lewej do prawej to w prawą stronę (1)
        self.attack_direction = 1

    def draw(self, surface):
        # Rysuj gracza + jego grafikę ataku
        surface.blit(pygame.transform.scale(self.image,ms.HERO_SIZE), self.rect)
        self.attack.draw(surface)

        # Rysuj tekst, jeśli wchodzimy w interakcję
        if self.interacted and self.interactable_text:
            for i,s in enumerate(str.split(self.interactable_text,';')):
                info_txt = ms.FONT_SMALL.render(s, True, ms.silver)
                info_txt_rect = info_txt.get_rect()

                info_txt_rect.centerx = (ms.WIDTH // 2)
                info_txt_rect.centery = ms.HEIGHT - 100 + (40 * i)
                surface.blit(info_txt, info_txt_rect)
        elif self.interactable_text:
            info_txt = ms.FONT_SMALL.render("Press E to interact", True, ms.silver)
            info_txt_rect = info_txt.get_rect()

            info_txt_rect.centerx = (ms.WIDTH // 2)
            info_txt_rect.centery = ms.HEIGHT - 40
            surface.blit(info_txt, info_txt_rect)


    def turn_left(self):
        self.rotate_left = True
        self.movement_x = -12


    def turn_right(self):
        self.rotate_left = False
        self.movement_x = 12

    def stop(self):
        self.movement_x = 0

    def clear(self):    # Zeruje akcje wykonywane przez gracza
        self.tickCounter = 0
        self.was_hit = False
        self.was_hit_trap = False
        self.press_right = False
        self.press_left = False
        self.movement_x = 0
        self.movement_y = 0

    def jump(self):
        self.rect.y += 2.5
        colliding_platforms = pygame.sprite.spritecollide(self, self.level.set_of_platforms, False)
        colliding_miscs = pygame.sprite.spritecollide(self,self.level.set_of_misc,False)
        self.rect.y -= 2.5
        if colliding_platforms or colliding_miscs:
            self.movement_y = self.jump_power
            if not pygame.mixer.Channel(2).get_busy():
                pygame.mixer.Channel(2).play(ms.JUMP_LIST[0])
        


    def update(self):

        #Zmniejsz życie jeśli zdrowie jest równe 0
        if self.health <= 0:
            self.lifes -= 1
            self.health = 2
            for p in self.level.set_of_platforms:
                if p.is_starting:
                    self.rect.x = p.rect.x + 80
                    self.rect.y = p.rect.top - 20
                    self.movement_y = 0
                    self.movement_x = 0
                    break

        self._gravitation() # Grawitacja

        # Ruch w poziomie
        self.rect.x += self.movement_x
        

        self.interactable_text = ""   # Jeśli nie znajdzie elementu do interakcji to nie bedzie tekstu

        # Kolizje z elementami otoczenia (oś X)
        colliding_miscs_pz = pygame.sprite.spritecollide(self,self.level.set_of_misc,False)
        if not self.was_hit and not self.was_hit_trap:
            for m in colliding_miscs_pz:
                # Jeśli wejdziemy w drzwi konczace poziom
                if m.winning_door:
                    self.level.won = True

                # Jeśli wejdziemy w obszar obiektu interaktywnego
                if m.text != "":
                    self.interactable_text = m.text

                # Jeśli obiekt obsługuje kolizje
                if m.collide and (self.rect.bottom > m.rect.top+1 and self.rect.top < m.rect.bottom+1):
                    if self.movement_x > 0:
                        self.rect.right = m.rect.left
                    if self.movement_x < 0:
                        self.rect.left = m.rect.right
                

                # Jeśli obiekt nie ma kolizji to wyczyść listę (potrzebne do obsługi animacji popychania)
                if not m.collide:
                    colliding_miscs_pz.clear()

        # Kolizje z platformami (oś X)
        colliding_platforms_pz = pygame.sprite.spritecollide(self, self.level.set_of_platforms, False) #Dla ruchu w poziomie
        if not self.was_hit and not self.was_hit_trap:
            for p in colliding_platforms_pz:
                if((self.rect.bottom > p.rect.top+1 and self.rect.top < p.rect.bottom+1)):
                    if self.movement_x > 0:
                        self.rect.right = p.rect.left
                        continue
                    if self.movement_x < 0:
                        self.rect.left = p.rect.right
                        continue
                colliding_platforms_pz.remove(p)
                    


        # Ruch w pionie
        self.rect.y += self.movement_y


        if self.rotate_left:
            self.attack.rect.right = self.rect.left
        else:
            self.attack.rect.left = self.rect.right
        self.attack.rect.y = self.rect.y

        # Animacje ciachnięcia mieczem
        if self.attack.is_slashing:
            if self.rotate_left:
                self.attack.Slash(ms.HERO_SLASH_LIST_L)
            else:
                self.attack.Slash(ms.HERO_SLASH_LIST_R)

        # Jeśli gracz wykonuje atak to zabron mu sie ruszac
        if self.attack.is_slashing:
            self.movement_x = 0
        else:
            if self.press_left:
                self.movement_x = -12
            elif self.press_right:
                self.movement_x = 12

        # Wykrywanie przeciwników / zabijanie ich
        if self.attack.is_slashing and not self.attack.slashed:
            colliding_enemies = pygame.sprite.spritecollide(self.attack, self.level.set_of_enemies, False)
            for e in colliding_enemies:   #Szukamy wykrytego przeciwnika
                for enemy in self.level.set_of_enemies:
                    if pygame.sprite.collide_rect(self.attack,enemy) and (not e.hit_anim or not e.death_anim):
                        if e.name == "Worm":
                            if not pygame.mixer.Channel(1).get_busy():
                                pygame.mixer.Channel(1).play(ms.WORM_DEATH_LIST[0])
                        elif e.name == "Mushroom":
                            if not pygame.mixer.Channel(1).get_busy():
                                pygame.mixer.Channel(1).play(ms.MUSHROOM_DEATH_LIST[0])
                        e.health -= 1
                        if e.health <= 0:
                            e.death_anim = True
                        elif e.health > 0:
                            e.hit_anim = True
                            e.count = 0
                        self.attack.slashed = True

        # Kolizja z przeciwnikiem (kiedy my zostaniemy przez niego trafieni)
        colliding_enemies = pygame.sprite.spritecollide(self, self.level.set_of_enemies, False)
        for e in colliding_enemies:  # Szukamy wykrytego przeciwnika
            for enemy in self.level.set_of_enemies:
                if pygame.sprite.collide_rect(self, enemy) and not self.was_hit and not e.death_anim:
                    self.was_hit = True
                    if e.movement_x > 0 and self.movement_x < 0:
                        self.attack_direction = 1
                    elif e.movement_x < 0 and self.movement_x > 0:
                        self.attack_direction = -1
                    elif e.movement_x < 0 and self.movement_x < 0:
                        self.attack_direction = 1
                    else:
                        self.attack_direction = -1

        if self.was_hit and self.tickCounter < 15:
            self.movement_x = 10 * self.attack_direction
            self.rect.y -= 9

            self.tickCounter += 1
        elif self.tickCounter >= 15 and self.was_hit:
            self.clear()
            self.health -= 1

        # Kolizje z elementami otoczenia (oś Y) / Kolizje z pułapkami
        colliding_miscs = pygame.sprite.spritecollide(self,self.level.set_of_misc,False)
        if not self.was_hit and not self.was_hit_trap:
            for m in colliding_miscs:
                if m.collide:
                    if self.movement_y > 0:
                        self.rect.bottom = m.rect.top
                    if self.movement_y < 0:
                        self.rect.top = m.rect.bottom
                    self.movement_y = 0

                # Pułapki (określenie w którą stronę cie odrzuci)
                elif m.trap:
                    self.was_hit_trap = True
                    if self.movement_x > 0:
                        self.attack_direction = -1
                    elif self.movement_x < 0:
                        self.attack_direction = 1
                    elif self.movement_x == 0:
                        self.attack_direction = -1
                if not m.collide:
                    colliding_miscs.clear()

        # Pułapki - odrzucenie gracza w przeciwną stronę
        if self.was_hit_trap and self.tickCounter < 15:
            self.movement_x = 10 * self.attack_direction
            if self.movement_x == 0:
                self.rect.y -= 15
            else:
                self.rect.y -= 9

            self.tickCounter += 1
        elif self.tickCounter >= 15 and self.was_hit_trap:
            self.clear() # Reset akcji gracza
            self.health -= 1


        # Kolizje z platformami (oś Y)
        colliding_platforms = pygame.sprite.spritecollide(self, self.level.set_of_platforms, False)
        for p in colliding_platforms:
            if colliding_platforms_pz.__contains__(p) == False:
                if self.movement_y > 0:
                    self.rect.bottom = p.rect.top
                    self.movement_y = 0
                elif self.movement_y < 0:
                    self.rect.top = p.rect.bottom
                    self.movement_y = 0


        # Animacje postaci
        if self.movement_x > 0 and self.attack.is_slashing:
            self._move(ms.HERO_SLASHING_LIST_R,idle=True) # Idle bo animacja ma 4 sprite'y tak samo jak animacje idle
        elif self.movement_x < 0 and self.attack.is_slashing:
            self._move(ms.HERO_SLASHING_LIST_L, idle=True)
        elif self.movement_x == 0 and self.attack.is_slashing:
            if self.rotate_left:
                self._move(ms.HERO_SLASHING_LIST_L, idle=True)
            else:
                self._move(ms.HERO_SLASHING_LIST_R, idle=True)
        elif self.movement_x > 0 and (len(colliding_platforms_pz) != 0 or len(colliding_miscs_pz) != 0) and len(colliding_platforms) != 0: # Można popychać rzeczy, kiedy listy obiektów
            self._move(ms.HERO_PUSH_LIST_R,push=True)                                                                                      # nie są puste (oczyszczamy je w ich pętlach)
        elif self.movement_x < 0 and (len(colliding_platforms_pz) != 0 or len(colliding_miscs_pz) != 0) and len(colliding_platforms) != 0:
            self._move(ms.HERO_PUSH_LIST_L,push=True)
        elif self.movement_x > 0 and (len(colliding_platforms) != 0 or len(colliding_miscs) != 0) :
            self._move(ms.HERO_RUN_LIST_R)
        elif self.movement_x < 0 and (len(colliding_platforms) != 0 or len(colliding_miscs) != 0):
            self._move(ms.HERO_RUN_LIST_L)
        elif self.movement_x == 0 and (len(colliding_platforms) != 0 or len(colliding_miscs) != 0):
            if self.rotate_left:
                self._move(ms.HERO_IDLE_LIST_L, idle=True)
            else:
                self._move(ms.HERO_IDLE_LIST_R, idle=True)

        # Zmiana grafik, gdy spadamy i skaczemy jeśli nie wykonujemy ataku
        if(self.attack.is_slashing == False):
            if self.movement_y > 0:
                if self.rotate_left:
                    self._move(ms.HERO_FALL_LIST_L, fall_jump=True)
                else:
                    self._move(ms.HERO_FALL_LIST_R, fall_jump=True)
            if self.movement_y < 0:
                if self.rotate_left:
                    self._move(ms.HERO_JUMP_LIST_L, fall_jump=True)
                else:
                    self._move(ms.HERO_JUMP_LIST_R, fall_jump=True)

        # Wykrywamy kolizje z przedmiotami
        colliding_items = pygame.sprite.spritecollide(self, self.level.set_of_items, False)
        for item in colliding_items:
            if item.name == "life":
                self.lifes += 1
                pygame.mixer.Channel(2).play(ms.LIFE_PICKUP[0])
                item.kill()
            if item.name == "health":
                self.health += 1
                pygame.mixer.Channel(2).play(ms.HEALTH_PICKUP[0])
                item.kill()
            if item.name == "gold":
                self.gold += 1
                pygame.mixer.Channel(0).play(ms.GOLD_PICKUP[0])
                item.kill()

        # Sprawdzamy czy gracz nie wypadl poza mape
        self._fall_death()

        # Pauzujemy akcje gracza jesli wcisnal przycisk interakcji
        if self.interacted and self.interactable_text:
            self.clear()
        else:
            self.interacted = False

    def _gravitation(self):
        if self.movement_y == 0:
            self.movement_y = 2.5
        else:
            self.movement_y += 0.45

    # Kiedy wypadniemy poza mapę
    def _fall_death(self):
        if(self.movement_y >= 50):
            self.lifes -= 1
            self.health = 2
            for p in self.level.set_of_platforms:
                if p.is_starting:
                    self.rect.x = p.rect.x + 80
                    self.rect.y = p.rect.top - 20
                    self.movement_y = 0
                    self.movement_x = 0
                    break

    # Obsługa zdarzeń / klawiatury
    def get_event(self, event):
        if not self.was_hit or not self.was_hit_trap: # Jeżeli nie otrzymujemy obrazen to mozemy sie poruszac
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not self.interacted: # Druga część wyrażenia blokuje ruch gracza, gdy wchodzi w interakcję z obiektem (wiadomości na tabliczkach)
                    self.press_left = True
                    self.turn_left()

                if event.key == pygame.K_RIGHT and not self.interacted:
                    self.press_right = True
                    self.turn_right()

                if event.key == pygame.K_UP and not self.interacted:
                     self.jump()

                if event.key == pygame.K_SPACE and not self.attack.is_slashing and not self.interacted: # Można atakować tylko jeśli nie wykonujemy ataku / nie czytamy interaktywnych wiadomości
                    self.attack.is_slashing = True
                    pygame.mixer.Channel(0).play(ms.SWING_LIST[random.randint(0,2)])

                if event.key == pygame.K_e:
                    self.interacted = not self.interacted

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if self.press_right:
                        self.turn_right()
                    else:
                        self.stop()
                    self.press_left = False

                if event.key == pygame.K_RIGHT:
                    if self.press_left:
                        self.turn_left()
                    else:
                        self.stop()
                    self.press_right = False

    # Zmiana grafik podczas animacji
    def _move(self, image_list,idle=False, fall_jump=False, push=False):

        if fall_jump:
            if self._count < 3:
                self.image = image_list[0]
            elif self._count < 6:
                self.image = image_list[1]
            elif self._count < 9:
                self.image = image_list[2]

            if self._count < 9:
                self._count += 1
            else:
                self._count = 0
        elif idle:
            if self._count < 3:
                self.image = image_list[0]
            elif self._count < 6:
                self.image = image_list[1]
            elif self._count < 9:
                self.image = image_list[2]
            elif self._count < 12:
                self.image = image_list[3]

            if self._count < 12:
                self._count += 1
            else:
                self._count = 0
        elif push:
            if self._count < 3:
                self.image = image_list[0]
            elif self._count < 6:
                self.image = image_list[1]
            elif self._count < 9:
                self.image = image_list[2]
            elif self._count < 12:
                self.image = image_list[3]
            elif self._count < 15:
                self.image = image_list[4]
            elif self._count < 18:
                self.image = image_list[5]

            if self._count < 18:
                self._count += 1
            else:
                self._count = 0
        else:
            if self._count < 3:
                self.image = image_list[0]
            elif self._count < 6:
                self.image = image_list[1]
            elif self._count < 9:
                self.image = image_list[2]
            elif self._count < 12:
                self.image = image_list[3]
            elif self._count < 15:
                self.image = image_list[4]

            if self._count < 15:
                self._count += 1
            else:
                self._count = 0