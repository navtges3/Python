from monster import *

class Quest:

    def __init__(self, name:str, description:str, monster_list:list[Monster], reward):
        self.name = name
        self.description = description
        self.reward = reward
        self.monster_list = monster_list
        self.monster_index = 0

    def next_monster(self) -> Monster:
        if self.monster_index < len(self.monster_list):
            monster = self.monster_list[self.monster_index]
            self.monster_index += 1
            return monster
        else:
            return None

    def get_monster(self) -> Monster:
        if self.monster_index < len(self.monster_list):
            return self.monster_list[self.monster_index]
        else:
            return None
        
    def is_complete(self) -> bool:
        return self.monster_index >= len(self.monster_list)