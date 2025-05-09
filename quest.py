from monster import *
from ui_helpers import *
import random

class Quest:

    def __init__(self, name:str, description:str, monster_list:dict, reward):
        self.name = name
        self.description = description
        self.reward = reward
        self.monster_list = monster_list
        self.monsters_slain = {}
        for key in monster_list:
            self.monsters_slain[key] = 0

    def get_monster(self) -> Monster:
        keys = []
        for key in self.monster_list.keys():
            if key in self.monsters_slain.keys():
                if self.monsters_slain[key] < self.monster_list[key]:
                    keys.append(key)
            else:
                keys.append(key)
        if len(keys) > 0:
            return get_monster(random.choice(keys))
        
    def slay_monster(self, monster:Monster) -> None:
        if monster.name in self.monsters_slain.keys():
            self.monsters_slain[monster.name] += 1

    def is_complete(self) -> bool:
        for key in self.monster_list.keys():
            if self.monsters_slain[key] < self.monster_list[key]:
                return False
        return True
    
    def draw(self, surface, font, button:Button):
        button.draw(surface, False, Colors.GOLD)
        draw_text(self.name, font, Colors.BLACK, surface, button.pos[0] + 10, button.pos[1] + 10)
        draw_wrapped_text(self.description, font, Colors.BLACK, surface, button.pos[0] + button.size[0] // 4, button.pos[1] + 10, button.size[0] // 2 - 20)
        
        output_text = ""
        for key in self.monster_list.keys():
            output_text += f"{key}: {self.monsters_slain[key]}/{self.monster_list[key]}\n"

        draw_multiple_lines(output_text, font, Colors.BLACK, surface, button.pos[0] + button.size[0] // 4 * 3, button.pos[1] + 10)