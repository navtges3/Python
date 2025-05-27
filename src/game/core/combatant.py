class Combatant:
    """Base class for all combatants in the game."""
    
    def __init__(self, name: str, max_hp: int) -> None:
        """Initialize a combatant.
        
        Args:
            name: The name of the combatant
            max_hp: Maximum hit points
        """
        self.name: str = name
        self.max_hp: int = max_hp
        self.current_hp: int = max_hp

    def is_alive(self) -> bool:
        """Check if the combatant is alive.
        
        Returns:
            True if current HP is greater than 0, False otherwise
        """
        return self.current_hp > 0
    
    def take_damage(self, damage: int) -> None:
        """Take damage and reduce current HP.
        
        Args:
            damage: Amount of damage to take
        """
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0