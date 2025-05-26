from constants import BattleState
from enum import Enum

class TurnState(Enum):
    HERO_TURN = 0
    MONSTER_TURN = 1

class BattleManager:
    def __init__(self, hero, battle_log):
        self.hero = hero
        self.battle_log = battle_log
        self.monster = None
        self.state = BattleState.HOME
        self.turn = TurnState.HERO_TURN  # Start with hero's turn

    def start_monster_turn(self):
        """Handle the monster's turn."""
        if self.monster and self.monster.is_alive():
            self.monster.attack(self.hero)
            self.battle_log.append(f"{self.monster.name} attacks {self.hero.name} for {self.monster.damage} damage.")
            self.turn = TurnState.HERO_TURN  # Switch back to hero's turn

    def handle_attack(self, monster):
        """Handle hero's attack action."""
        if self.turn != TurnState.HERO_TURN:
            return  # Not hero's turn
            
        self.hero.attack(monster)
        self.battle_log.append(f"{self.hero.name} attacks {monster.name} with {self.hero.weapon.name} for {self.hero.weapon.damage + self.hero.potion_damage} damage.")
        if self.hero.potion_damage > 0:
            self.hero.potion_damage = 0
            
        # Switch to monster's turn
        self.turn = TurnState.MONSTER_TURN
        if monster.is_alive():
            self.start_monster_turn()

    def handle_defend(self):
        """Handle hero's defend action."""
        if self.turn != TurnState.HERO_TURN:
            return  # Not hero's turn
            
        self.hero.potion_block += 5
        self.battle_log.append(f"{self.hero.name} takes a defensive stance!")
        
        # Switch to monster's turn
        self.turn = TurnState.MONSTER_TURN
        if self.monster and self.monster.is_alive():
            self.start_monster_turn()

    def handle_use_potion(self):
        """Handle hero's potion use."""
        if self.turn != TurnState.HERO_TURN:
            return  # Not hero's turn
        self.state = BattleState.USE_ITEM
        # Note: Turn state doesn't change until potion is actually used

    def handle_flee(self):
        """Handle hero's flee action."""
        if self.turn != TurnState.HERO_TURN:
            return False  # Not hero's turn
        self.state = BattleState.RUN_AWAY
        return True  # Successful flee