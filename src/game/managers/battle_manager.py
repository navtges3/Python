from src.game.core.constants import GameState
from src.game.entities.monster import Monster
from src.game.entities.hero import Hero
from enum import Enum
from src.game.managers.button_manager import ButtonManager


class TurnState(Enum):
    HERO_TURN = 0
    MONSTER_TURN = 1

class BattleState(Enum):
    HOME = 0
    USE_ITEM = 1
    RUN_AWAY = 2
    MONSTER_DEFEATED = 3

class BattleManager:
    def __init__(self, hero: Hero, battle_log: list):
        self.hero = hero
        self.battle_log = battle_log
        self.monster = None
        self.state = BattleState.HOME
        self.turn = TurnState.HERO_TURN  # Start with hero's turn

    def start_battle(self, monster: Monster):
        """Initialize a new battle with a monster."""
        self.monster = monster
        self.state = BattleState.HOME  # Reset to HOME state for new battle
        self.turn = TurnState.HERO_TURN
        self.battle_log.append(f"A {self.monster.name} appears!")

    def update_battle_state(self):
        """Update the battle state and check for victory/defeat conditions."""
        # Only check for monster defeat if we're in an active battle
        if self.state != BattleState.MONSTER_DEFEATED:
            if self.hero.is_alive() and not self.monster.is_alive():
                self.handle_monster_defeat()
                return True  # Monster defeated
            elif not self.hero.is_alive():
                return False  # Hero defeated
        return None  # Battle continues

    def handle_monster_defeat(self):
        """Handle monster defeat logic."""
        self.battle_log.append(f"{self.monster.name} has been defeated!")
        self.battle_log.append(f"{self.hero.name} gains {self.monster.experience} experience and {self.monster.gold} gold.")
        self.hero.gain_experience(self.monster.experience)
        self.hero.add_gold(self.monster.gold)
        self.state = BattleState.MONSTER_DEFEATED

    def update_button_states(self, button_manager: ButtonManager):
        """Update battle button states based on current turn and battle state."""
        if self.state == BattleState.MONSTER_DEFEATED:
            # Lock combat buttons, unlock victory buttons
            for name in ['Attack', 'Defend', 'Use Potion', 'Flee']:
                button = button_manager.get_button(GameState.BATTLE, name)
                button.lock()
            for name in ['Continue', 'Retreat']:
                button = button_manager.get_button(GameState.BATTLE, name)
                button.unlock()
        else:
            # Lock victory buttons
            for name in ['Continue', 'Retreat']:
                button = button_manager.get_button(GameState.BATTLE, name)
                button.lock()
                
            if self.turn == TurnState.MONSTER_TURN:
                # Lock all hero action buttons during monster's turn
                for name in ['Attack', 'Defend', 'Use Potion', 'Flee']:
                    button = button_manager.get_button(GameState.BATTLE, name)
                    button.lock()
                self.start_monster_turn()
            else:  # Hero's turn
                if self.state == BattleState.HOME:
                    # Unlock basic combat buttons
                    for name in ['Attack', 'Defend', 'Flee']:
                        button = button_manager.get_button(GameState.BATTLE, name)
                        button.unlock()
                    # Handle potion button separately
                    use_potion_button = button_manager.get_button(GameState.BATTLE, "Use Potion")
                    if self.hero.has_potions():
                        use_potion_button.unlock()
                    else:
                        use_potion_button.lock()

    def handle_monster_attack(self):
        """Handle monster's attack action."""
        if self.turn != TurnState.MONSTER_TURN:
            return  # Not monster's turn
            
        if self.monster and self.monster.is_alive():
            # Calculate damage after hero's block
            damage = max(0, self.monster.damage - self.hero.potion_block)
            self.hero.take_damage(damage)
            
            # Create battle log message
            if self.hero.potion_block > 0:
                self.battle_log.append(f"{self.hero.name} blocks {self.hero.potion_block} damage!")
                self.battle_log.append(f"{self.monster.name} attacks {self.hero.name} for {damage} damage.")
            else:
                self.battle_log.append(f"{self.monster.name} attacks {self.hero.name} for {damage} damage.")
            
            # Reset hero's block after the attack
            self.hero.potion_block = 0
            
            # Switch back to hero's turn
            self.turn = TurnState.HERO_TURN

    def start_monster_turn(self):
        """Handle the monster's turn."""
        if self.monster and self.monster.is_alive():
            self.handle_monster_attack()

    def handle_attack(self, monster: Monster):
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