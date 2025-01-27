from Monsters.MonsterBase import monsterBase

class goblin(monsterBase):
    def __init__(self, health, damage):
        super().__init__("Goblin", health, damage)