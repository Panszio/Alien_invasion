import sys
import pygame as py
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_Stats import GameStats  # Dodaj import klasy GameStats

class AlienInvasion:
    """Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania"""

    def __init__(self):
        """Inicjalizacja gry"""
        py.init()
        self.clock = py.time.Clock()
        self.settings = Settings()

        self.screen = py.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        py.display.set_caption("Inwazja Obcych")

        self.stats = GameStats(self)  # Inicjalizacja statystyk gry

        self.ship = Ship(self)

        self.bullets = py.sprite.Group()
        self.aliens = py.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Rozpoczęcie Głównej Pętli"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == py.KEYUP:
                self._check_keyup_events(event)

    def _create_fleet(self):
        """Utworzenie pełnej floty"""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Utwórz obcego i umieść go w rzędzie."""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_keydown_events(self, event):
        """Reaguj na naciśnięcia klawiszy."""
        if event.key == py.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == py.K_LEFT:
            self.ship.moving_left = True
        elif event.key == py.K_SPACE:
            self._fire_bullet()
        elif event.key == py.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Reaguj na zwolnienia klawiszy."""
        if event.key == py.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == py.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Utwórz nowy pocisk i dodaj go do grupy pocisków."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Uaktualnij pozycje pocisków i pozbądź się starych pocisków."""
        self.bullets.update()

        # Usuń pociski, które wyszły poza ekran.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Sprawdź kolizje między pociskami a kosmitami.
        collisions = py.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Usuń istniejące pociski i utwórz nową flotę.
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """Uaktualnij pozycje wszystkich obcych w flocie."""
        self._check_fleet_edges()
        self.aliens.update()

        # Sprawdź kolizje między kosmitami a statkiem.
        if py.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Sprawdź, czy któryś z kosmitów dotarł do dolnej krawędzi ekranu.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Reaguj odpowiednio, gdy obcy dotrze do krawędzi ekranu."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Przenieś całą flotę w dół i zmień jej kierunek."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Reaguj na kolizję statku z kosmitą."""
        if self.stats.ships_left > 0:
            # Zmniejsz ships_left.
            self.stats.ships_left -= 1

            # Usuń wszystkich kosmitów i pociski.
            self.aliens.empty()
            self.bullets.empty()

            # Utwórz nową flotę i wyśrodkuj statek.
            self._create_fleet()
            self.ship.center_ship()

            # Pauza.
            py.time.sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """Sprawdź, czy którykolwiek kosmita dotarł do dolnej krawędzi ekranu."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Traktuj to tak, jakby statek został trafiony.
                self._ship_hit()
                break

    def _update_screen(self):
        """Uaktualnij obrazy na ekranie i przełącz na nowy ekran."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        py.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
