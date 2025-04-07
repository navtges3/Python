from hero import Hero
from monster import Monster, get_monster
from constants import GameState
from screens import Screens

def main() -> None:
    hero:Hero = None
    monster:Monster = None
    # Initialize the game
    screen = Screens()
    state = GameState.WELCOME
    while state != GameState.GAME_OVER:
        if state == GameState.WELCOME:
            state, hero = screen.welcome_screen()
        elif state == GameState.NEW_GAME:
            state, hero = screen.new_game_screen()
        elif state == GameState.MAIN_GAME:
            state = screen.main_game(hero)
        elif state == GameState.BATTLE:
            monster = get_monster(hero.level)
            state = screen.battle_screen(hero, monster)
        elif state == GameState.SHOP:
            state = screen.shop_screen(hero)
        else:
            state = GameState.GAME_OVER
    
    screen.quit()

if __name__ == "__main__":
    main()