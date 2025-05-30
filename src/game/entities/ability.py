from typing import Optional, List, Dict, Any
from src.game.core.combatant import Combatant
from dataclasses import dataclass
from random import random

@dataclass
class AbilityEffect:
    """Represents the effects of an ability."""
    damage: int = 0
    healing: int = 0
    block: int = 0
    duration: int = 1  # Number of turns the effect lasts
    missed: bool = False
    critical: bool = False

class Ability:
    """Base class for all abilities in the game."""
    
    def __init__(self, 
                name: str,
                description: str,
                cooldown: int,
                energy_cost: int) -> None:
        """
        Initialize an ability.
        
        Args:
            name: Name of the ability
            description: Description of what the ability does
            cooldown: Number of turns before ability can be used again
            energy_cost: Amount of energy required to use the ability
        """
        self.name: str = name
        self.description: str = description
        self.cooldown: int = cooldown
        self.energy_cost: int = energy_cost
        self.current_cooldown: int = 0
        
    def can_use(self, user: Combatant) -> bool:
        """Check if the ability can be used."""
        return self.current_cooldown == 0
    
    def update_cooldown(self) -> None:
        """Update the ability's cooldown at the end of a turn."""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
            
    def use(self, user: Combatant, target: Optional[Combatant] = None) -> AbilityEffect:
        """
        Use the ability.
        
        Args:
            user: The combatant using the ability
            target: The target of the ability (if any)
            
        Returns:
            AbilityEffect containing the results of using the ability
        """
        if not self.can_use(user):
            raise ValueError(f"{self.name} is still on cooldown!")
        
        self.current_cooldown = self.cooldown
        return AbilityEffect()
    
    def __str__(self) -> str:
        return f"{self.name} ({self.energy_cost} energy, {self.cooldown} turn cooldown)"

class AttackAbility(Ability):
    """An ability that deals damage to a target."""
    
    def __init__(self,
                name: str,
                description: str,
                damage_multiplier: float,
                accuracy_modifier: float,
                crit_chance_modifier: float,
                crit_damage_modifier: float,
                cooldown: int,
                energy_cost: int) -> None:
        """
        Initialize an attack ability.
        
        Args:
            damage_multiplier: Multiplier applied to weapon damage
            accuracy_modifier: Modifier applied to weapon accuracy
            crit_chance_modifier: Modifier applied to weapon crit chance
            crit_damage_modifier: Modifier applied to weapon crit damage
        """
        super().__init__(name, description, cooldown, energy_cost)
        self.damage_multiplier: float = damage_multiplier
        self.accuracy_modifier: float = accuracy_modifier
        self.crit_chance_modifier: float = crit_chance_modifier
        self.crit_damage_modifier: float = crit_damage_modifier
        
    def use(self, user: Combatant, target: Optional[Combatant] = None) -> AbilityEffect:
        """Use the attack ability on a target."""
        if target is None:
            raise ValueError("Attack abilities require a target!")
            
        # Runtime type checking instead of static typing
        if not hasattr(user, 'weapon'):
            raise ValueError("Attack abilities can only be used by heroes with weapons!")
            
        if not user.weapon:
            raise ValueError("Hero must have a weapon equipped!")
            
        effect = super().use(user, target)
        
        # Calculate modified weapon stats
        accuracy = min(1.0, user.weapon.accuracy * self.accuracy_modifier)
        crit_chance = min(1.0, user.weapon.crit_chance * self.crit_chance_modifier)
        crit_damage = user.weapon.crit_damage * self.crit_damage_modifier
        base_damage = int(user.weapon.damage * self.damage_multiplier)
        
        # Check for miss
        if random() > accuracy:
            effect.missed = True
            effect.damage = 0
            return effect
            
        # Check for critical hit
        if random() < crit_chance:
            effect.critical = True
            effect.damage = int(base_damage * crit_damage)
        else:
            effect.damage = base_damage
            
        # Apply damage to target
        if target:
            target.take_damage(effect.damage)
            
        return effect

class DefendAbility(Ability):
    """An ability that provides defensive benefits."""
    
    def __init__(self,
                name: str,
                description: str,
                block_amount: int,
                duration: int,
                cooldown: int,
                energy_cost: int) -> None:
        """
        Initialize a defend ability.
        
        Args:
            block_amount: Amount of damage blocked
            duration: Number of turns the block lasts
        """
        super().__init__(name, description, cooldown, energy_cost)
        self.block_amount: int = block_amount
        self.duration: int = duration
        
    def use(self, user: Combatant, target: Optional[Combatant] = None) -> AbilityEffect:
        """Use the defend ability."""
        effect = super().use(user, target)
        effect.block = self.block_amount
        effect.duration = self.duration
        return effect

class UtilityAbility(Ability):
    """An ability that provides utility effects like healing or buffs."""
    
    def __init__(self,
                name: str,
                description: str,
                healing: int,
                cooldown: int,
                energy_cost: int) -> None:
        """
        Initialize a utility ability.
        
        Args:
            healing: Amount of healing provided
        """
        super().__init__(name, description, cooldown, energy_cost)
        self.healing: int = healing
        
    def use(self, user: Combatant, target: Optional[Combatant] = None) -> AbilityEffect:
        """Use the utility ability."""
        effect = super().use(user, target)
        effect.healing = self.healing
        
        # Apply healing to the target (or self if no target)
        target_to_heal = target if target else user
        target_to_heal.current_hp = min(
            target_to_heal.current_hp + effect.healing,
            target_to_heal.max_hp
        )
        
        return effect