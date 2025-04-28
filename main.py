from constants import Game_State
from game import Game

def main() -> None:
    my_game = Game()
    while my_game.game_state != Game_State.EXIT:
        if my_game.game_state == Game_State.WELCOME:
            my_game.welcome_screen()
        elif my_game.game_state == Game_State.NEW_GAME:
            my_game.new_game_screen()
        elif my_game.game_state == Game_State.MAIN_GAME:
            my_game.main_game()
        elif my_game.game_state == Game_State.BATTLE:
            my_game.battle_screen()
        elif my_game.game_state == Game_State.SHOP:
            my_game.shop_screen()
        elif my_game.game_state == Game_State.GAME_OVER:
            my_game.game_over_screen()
    
    my_game.quit()

if __name__ == "__main__":
    main()