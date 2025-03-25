class Village:
    def __init__(self, name:str, health:int=100):
        self.name = name
        self.health = health

    def take_damage(self, damage:int):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"The village {self.name} takes {damage} damage! Remaining health: {self.health}")

    def is_destroyed(self) -> bool:
        return self.health <= 0