from src.game.core.constants import GameState
from src.game.entities.monster import Monster
from src.game.entities.hero import Hero
from src.game.entities.items import potion_dictionary
from src.game.ui.tooltip import Tooltip
from enum import Enum
from src.game.managers.button_manager import ButtonManager
from typing import Optional, List


class TurnState(Enum):
    HERO_TURN = 0
    MONSTER_TURN = 1

class BattleState(Enum):
    HOME = 0
    USE_ITEM = 1
    RUN_AWAY = 2
    MONSTER_DEFEATED = 3

class BattleManager:
    def __init__(self, hero: Hero, battle_log: List[str]) -> None:
        """Initialize the battle manager.
        
        Args:
            hero: The player's hero character
            battle_log: List to store battle messages
        """
        self.hero: Hero = hero
        self.battle_log: List[str] = battle_log
        self.monster: Optional[Monster] = None
        self.state: BattleState = BattleState.HOME
        self.turn: TurnState = TurnState.HERO_TURN  # Start with hero's turn
        self.showing_potions: bool = False  # Track if potion buttons are visible
        self.button_manager: Optional[ButtonManager] = None  # Store button manager reference
        self.tooltip: Optional[Tooltip] = None  # Store current tooltip

    def start_battle(self, monster: Monster) -> None:
        """Initialize a new battle with a monster.
        
        Args:
            monster: The monster to battle against
        """
        self.monster = monster
        self.state = BattleState.HOME  # Reset to HOME state for new battle
        self.turn = TurnState.HERO_TURN
        self.battle_log.append(f"A {self.monster.name} appears!")

    def update_battle_state(self) -> Optional[bool]:
        """Update the battle state and check for victory/defeat conditions.
        
        Returns:
            True if monster was defeated
            False if hero was defeated
            None if battle continues
        """
        # Only check for monster defeat if we're in an active battle
        if self.state != BattleState.MONSTER_DEFEATED:
            if self.hero.is_alive() and not self.monster.is_alive():
                self.handle_monster_defeat()
                return True  # Monster defeated
            elif not self.hero.is_alive():
                return False  # Hero defeated
        return None  # Battle continues

    def handle_monster_defeat(self) -> None:
        """Handle monster defeat logic."""
        if not self.monster:
            return
        self.battle_log.append(f"{self.monster.name} has been defeated!")
        self.battle_log.append(f"{self.hero.name} gains {self.monster.experience} experience and {self.monster.gold} gold.")
        self.hero.gain_experience(self.monster.experience)
        self.hero.add_gold(self.monster.gold)
        self.state = BattleState.MONSTER_DEFEATED

    def update_button_states(self, button_manager: ButtonManager) -> None:
        """Update battle button states based on current turn and battle state.
        
        Args:
            button_manager: The button manager to update button states
        """
        # Store button manager reference for use in other methods
        self.button_manager = button_manager
        
        if self.state == BattleState.MONSTER_DEFEATED:
            # Lock combat buttons, unlock victory buttons
            for name in ['Attack', 'Defend', 'Potion', 'Flee']:
                button = button_manager.get_button(GameState.BATTLE, name)
                button.lock()
            for name in ['Continue', 'Retreat']:
                button = button_manager.get_button(GameState.BATTLE, name)
                button.unlock()
            # Hide potion buttons if they were showing
            self._toggle_potion_buttons(button_manager, False)
        else:
            # Lock victory buttons
            for name in ['Continue', 'Retreat']:
                button = button_manager.get_button(GameState.BATTLE, name)
                button.lock()
                
            if self.turn == TurnState.MONSTER_TURN:
                # Lock all hero action buttons during monster's turn
                for name in ['Attack', 'Defend', 'Potion', 'Flee']:
                    button = button_manager.get_button(GameState.BATTLE, name)
                    button.lock()
                # Hide potion buttons if they were showing
                self._toggle_potion_buttons(button_manager, False)
                self.start_monster_turn()
            else:  # Hero's turn
                if self.state == BattleState.HOME:
                    # Unlock basic combat buttons
                    for name in ['Attack', 'Defend', 'Flee']:
                        button = button_manager.get_button(GameState.BATTLE, name)
                        button.unlock()
                    # Handle potion button separately
                    potions_button = button_manager.get_button(GameState.BATTLE, "Potion")
                    if self.hero.has_potions():
                        potions_button.unlock()
                    else:
                        potions_button.lock()
                    # Update potion selection buttons if they're showing
                    if self.showing_potions:
                        self._update_potion_button_states(button_manager)
                elif self.state == BattleState.USE_ITEM:
                    # Lock combat buttons except Potion
                    for name in ['Attack', 'Defend', 'Flee']:
                        button = button_manager.get_button(GameState.BATTLE, name)
                        button.lock()
                    # Show and update potion selection buttons
                    self._toggle_potion_buttons(button_manager, True)
                    self._update_potion_button_states(button_manager)

    def get_potion_tooltip(self, potion_name: str) -> Optional[Tooltip]:
        """Get tooltip for a potion button.
        
        Args:
            potion_name: Name of the potion to get tooltip for
            
        Returns:
            Tooltip object if potion exists, None otherwise
        """
        if self.button_manager and potion_name in potion_dictionary:
            potion = potion_dictionary[potion_name]
            return Tooltip(f"{potion.description} (x{self.hero.potion_bag[potion_name]})", self.button_manager.font)
        return None

    def _toggle_potion_buttons(self, button_manager: ButtonManager, show: bool) -> None:
        """Show or hide potion selection buttons.
        
        Args:
            button_manager: The button manager to update button states
            show: Whether to show or hide the buttons
        """
        self.showing_potions = show
        for name in ['Health Potion', 'Damage Potion', 'Block Potion']:
            button = button_manager.get_button(GameState.BATTLE, name)
            if show:
                button.show()
            else:
                button.hide()

    def _update_potion_button_states(self, button_manager: ButtonManager) -> None:
        """Update potion selection button states based on inventory.
        
        Args:
            button_manager: The button manager to update button states
        """
        for potion_name in ['Health Potion', 'Damage Potion', 'Block Potion']:
            button = button_manager.get_button(GameState.BATTLE, potion_name)
            if self.hero.potion_bag[potion_name] > 0:
                button.unlock()
            else:
                button.lock()

    def handle_monster_attack(self) -> None:
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

    def start_monster_turn(self) -> None:
        """Handle the monster's turn."""
        if self.monster and self.monster.is_alive():
            self.handle_monster_attack()

    def handle_attack(self, monster: Monster) -> None:
        """Handle hero's attack action.
        
        Args:
            monster: The monster to attack
        """
        if self.turn != TurnState.HERO_TURN:
            return  # Not hero's turn
            
        damage, missed, crit = self.hero.attack(monster)
        
        # Add appropriate battle log message based on the attack result
        if missed:
            self.battle_log.append(f"{self.hero.name}'s attack with {self.hero.weapon.name} missed!")
        else:
            if crit:
                self.battle_log.append(f"{self.hero.name} lands a critical hit with {self.hero.weapon.name}!")
            self.battle_log.append(f"{self.hero.name} attacks {monster.name} for {damage + self.hero.potion_damage} damage.")
            
        if self.hero.potion_damage > 0:
            self.hero.potion_damage = 0
            
        # Switch to monster's turn
        self.turn = TurnState.MONSTER_TURN
        if monster.is_alive():
            self.start_monster_turn()

    def handle_defend(self) -> None:
        """Handle hero's defend action."""
        if self.turn != TurnState.HERO_TURN:
            return  # Not hero's turn
            
        self.hero.potion_block += 5
        self.battle_log.append(f"{self.hero.name} takes a defensive stance!")
        
        # Switch to monster's turn
        self.turn = TurnState.MONSTER_TURN
        if self.monster and self.monster.is_alive():
            self.start_monster_turn()

    def handle_use_potion(self) -> None:
        """Handle hero's potion use."""
        if self.turn != TurnState.HERO_TURN or not self.button_manager:
            return  # Not hero's turn or no button manager
            
        # Toggle between showing and hiding potion buttons
        if self.state == BattleState.USE_ITEM:
            self.state = BattleState.HOME
            self._toggle_potion_buttons(self.button_manager, False)
        else:
            self.state = BattleState.USE_ITEM
            self._toggle_potion_buttons(self.button_manager, True)
        # Note: Turn state doesn't change until potion is actually used

    def use_potion(self, potion_name: str) -> None:
        """Use a specific potion.
        
        Args:
            potion_name: Name of the potion to use
        """
        if self.turn != TurnState.HERO_TURN or self.state != BattleState.USE_ITEM or not self.button_manager:
            return  # Not in correct state to use potion
            
        self.hero.use_potion(potion_name)
        self.battle_log.append(f"{self.hero.name} used a {potion_name}!")
        
        # Hide potion buttons after use
        self._toggle_potion_buttons(self.button_manager, False)
        
        # Return to normal battle state and switch turns
        self.state = BattleState.HOME
        self.turn = TurnState.MONSTER_TURN
        if self.monster and self.monster.is_alive():
            self.start_monster_turn()

    def handle_flee(self) -> bool:
        """Handle hero's flee action.
        
        Returns:
            bool: True if flee was successful, False otherwise
        """
        if self.turn != TurnState.HERO_TURN:
            return False  # Not hero's turn
        self.state = BattleState.RUN_AWAY
        return True  # Successful flee