from typing import Dict
from src.game.entities.ability import Ability, AttackAbility, DefendAbility

# Dictionary containing all attack abilities
attack_abilities: Dict[str, Ability] = {
    "Precise Strike": AttackAbility(
        name="Precise Strike",
        description="A precise attack with increased accuracy",
        damage_multiplier=1.0,
        accuracy_modifier=1.5,
        crit_chance_modifier=1.2,
        crit_damage_modifier=1.0,
        cooldown=2,
        energy_cost=2
    ),
    "Power Attack": AttackAbility(
        name="Power Attack",
        description="A powerful but less accurate attack",
        damage_multiplier=1.5,
        accuracy_modifier=0.8,
        crit_chance_modifier=1.0,
        crit_damage_modifier=1.2,
        cooldown=3,
        energy_cost=3
    ),
    "Critical Strike": AttackAbility(
        name="Critical Strike",
        description="An attack focused on landing critical hits",
        damage_multiplier=1.0,
        accuracy_modifier=1.0,
        crit_chance_modifier=2.0,
        crit_damage_modifier=1.5,
        cooldown=4,
        energy_cost=4
    ),
}

# Dictionary containing all defense abilities
defense_abilities: Dict[str, Ability] = {
    "Guard": DefendAbility(
        name="Guard",
        description="Take a defensive stance",
        block_amount=8,
        duration=2,
        cooldown=2,
        energy_cost=2
    ),
    "Shield Wall": DefendAbility(
        name="Shield Wall",
        description="Create a strong defensive barrier",
        block_amount=12,
        duration=1,
        cooldown=4,
        energy_cost=3
    ),
}
