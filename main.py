from src.game.core.constants import GameState
from src.game.core.game import Game

def main() -> None:
    my_game = Game()
    while my_game.game_state != GameState.EXIT:
        if my_game.game_state == GameState.WELCOME:
            my_game.welcome_screen()
        elif my_game.game_state == GameState.NEW_GAME:
            my_game.new_game_screen()
        elif my_game.game_state == GameState.MAIN_GAME:
            my_game.main_game()
        elif my_game.game_state == GameState.QUEST:
            my_game.quest_screen()
        elif my_game.game_state == GameState.BATTLE:
            my_game.battle_screen()
        elif my_game.game_state == GameState.SHOP:
            my_game.shop_screen()
        elif my_game.game_state == GameState.VICTORY:
            my_game.victory_screen()
        elif my_game.game_state == GameState.DEFEAT:
            my_game.defeat_screen()
    
    my_game.quit()

if __name__ == "__main__":
    main()