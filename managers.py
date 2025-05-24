from constants import BattleState

class BattleManager:
    def __init__(self, hero, battle_log):
        self.hero = hero
        self.battle_log = battle_log
        self.monster = None
        self.state = BattleState.HOME

    def handle_attack(self, monster):
        self.hero.attack(monster)
        self.battle_log.append(f"{self.hero.name} attacks {monster.name} with {self.hero.weapon.name} for {self.hero.weapon.damage + self.hero.potion_damage} damage.")
        if self.hero.potion_damage > 0:
            self.hero.potion_damage = 0
        if monster.is_alive():
            monster.attack(self.hero)
            self.battle_log.append(f"{monster.name} attacks {self.hero.name} for {monster.damage} damage.")