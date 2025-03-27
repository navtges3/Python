from hero import Hero
from constants import GameState
from screens import Screens
import json

def main() -> None:
    hero:Hero = None
    screen = Screens()
    state = GameState.WELCOME
    while state != GameState.GAME_OVER:
        if state == GameState.WELCOME:
            state = screen.welcome_screen()
        elif state == GameState.NEW_GAME:
            state, hero = screen.new_game_screen()
        elif state == GameState.MAIN_GAME:
            state = screen.main_game(hero)
        else:
            state = GameState.GAME_OVER
    
    screen.quit()

if __name__ == "__main__":
    main()