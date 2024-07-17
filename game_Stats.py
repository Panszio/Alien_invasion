class GameStats:
    """Monitorowanie statystyk gry."""

    def __init__(self, ai_game):
        """Inicjalizacja statystyk."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Rozpocznij grę w stanie aktywnym.
        self.game_active = True

    def reset_stats(self):
        """Inicjalizacja danych statystycznych, które mogą zmienić się w trakcie gry."""
        self.ships_left = self.settings.ship_limit
