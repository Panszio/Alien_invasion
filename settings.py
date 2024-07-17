class Settings:
    """Klasa do przechowywania wszystkich ustawień gry."""

    def __init__(self):
        """Inicjalizacja ustawień gry."""
        # Ustawienia ekranu
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ustawienia statku
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Ustawienia pocisków
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 5

        # Ustawienia obcych
        self.alien_speed = 5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 oznacza ruch w prawo, -1 oznacza ruch w lewo
