
class Combatant:
    def __init__(self, name, max_hp):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp

    def is_alive(self) -> int:
        return self.current_hp > 0
    
    def take_damage(self, damage:int) -> None:
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0