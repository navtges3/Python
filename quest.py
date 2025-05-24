from monster import *
from ui_helpers import *
import random

class Quest:

    def __init__(self, name:str, description:str, monster_list:dict, reward, penalty):
        self.name = name
        self.reward = reward
        self.penalty = penalty
        self.description = description
        self.monster_list = monster_list
        self.monsters_slain = {}
        for key in monster_list:
            self.monsters_slain[key] = 0

    def get_monster(self) -> Monster:
        living_monsters = []
        for key in self.monster_list.keys():
            if key in self.monsters_slain.keys():
                if self.monsters_slain[key] < self.monster_list[key]:
                    living_monsters.append(key)
            else:
                living_monsters.append(key)
        if len(living_monsters) > 0:
            return get_monster(random.choice(living_monsters))
        
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

class QuestButton(Button):
    def __init__(self, quest: Quest, pos, size, font, text_color):
        quest_image_path = fileIO.resource_path("images\\buttons\\quest_background.png")
        super().__init__("QuestButton", pos, size, font, text_color, background_image_path=quest_image_path, hover_image_path=quest_image_path)
        self.quest = quest

    def draw(self, surface):
        border_color = Colors.GOLD if self.selected else Colors.BLACK
        
        if self.quest.is_complete():
            self.button_color = Colors.GREEN
            self.hover_color = Colors.LIGHT_GREEN

        super().draw(surface, False, border_color)

        # Use self.rect.x and self.rect.y for dynamic positioning
        draw_text(self.quest.name, self.font, Colors.BLACK, surface, self.rect.x + 10, self.rect.y + 10)
        draw_text(self.quest.reward.name, self.font, Colors.GREEN, surface, self.rect.x + 10, self.rect.y + 40)
        draw_text(str(self.quest.penalty), self.font, Colors.RED, surface, self.rect.x + 10, self.rect.y + 70)

        draw_wrapped_text(self.quest.description, self.font, Colors.BLACK, surface, self.rect.x + self.rect.width // 3, self.rect.y + 10, self.rect.width // 3 + 50)

        output_text = ""
        for key in self.quest.monster_list.keys():
            output_text += f"{key}: {self.quest.monsters_slain[key]}/{self.quest.monster_list[key]}\n"

        draw_multiple_lines(output_text, self.font, Colors.BLACK, surface, self.rect.x + self.rect.width // 4 * 3 + 25, self.rect.y + 10)

quest_list = {
    # Quest 1
    Quest("Village Under Siege", "Defend the villagers by eliminating four goblins and two orcs.", {"Goblin": 4,"Orc": 2,}, potion_dictionary["Block Potion"], ("village", -10)),
    # Quest 2
    Quest("Goblin Infestation", "A horde of goblins threatens the farms! Defeat six goblins to secure the land.", {"Goblin": 6,}, potion_dictionary["Health Potion"], ("village", -10)),
    # Quest 3
    Quest("Ogre Troubles", "Ogres have taken control of the mines. Slay three to reclaim the tunnels!", {"Ogre": 3,}, potion_dictionary["Damage Potion"], ("village", -10)),
    # Quest 4
    Quest("Bridge of Peril", "A goblin warband and their ogre leader guard the bridge. Eliminate them and restore safe passage.", {"Goblin": 3,"Ogre": 1,}, potion_dictionary["Block Potion"], ("village", -10)),
    # Quest 5
    Quest("The Forest Menace", "Patrol the woods and eliminate five goblins and their ogre brute.", {"Goblin": 5,"Ogre": 1,}, potion_dictionary["Health Potion"], ("village", -10)),
    # Quest 6
    Quest("Guardian of the Ruins", "The ruins hold secrets, but goblins and ogres stand in your way. Defeat them!", {"Goblin": 2,"Ogre": 2,}, potion_dictionary["Damage Potion"], ("village", -10)),
    # Quest 7
    Quest("Rampaging Goblins", "A large group of goblins terrorizes the countryside. Take down seven!", {"Goblin": 7,}, potion_dictionary["Block Potion"], ("village", -10)),
    # Quest 8
    Quest("Cave Dweller’s Wrath", "Deep in the caves, ogres and goblins lurk. Destroy two goblins and four ogres.", {"Goblin": 2,"Ogre": 4,}, potion_dictionary["Damage Potion"], ("village", -10)),
    # Quest 9
    Quest("Battle at Dawn", "A mixed force of goblins, ogres, and orcs is preparing for an assault. Strike first!", {"Goblin": 3,"Ogre": 2,"Orc": 2,}, potion_dictionary["Block Potion"], ("village", -10)),
    # Quest 10
    Quest("End of the Horde", "Wipe out the remaining goblin forces, their ogre champions, and the orc warlord!", {"Goblin": 6,"Ogre": 3,"Orc": 1,}, potion_dictionary["Health Potion"], ("village", -10)),
}
