from src.game.entities.monster import *
from src.game.ui.ui_helpers import *
from src.game.ui.spritesheet import SpriteSheet
from src.game.entities.items import potion_dictionary, Item
import random
import pygame
from typing import Dict, Optional, Tuple, List, Set, Union

# Type aliases
MonsterCount = Dict[str, int]
QuestReward = Item
QuestPenalty = Tuple[str, int]

class Quest:
    """A class representing a quest that can be undertaken by the hero."""

    def __init__(self, name: str, description: str, monster_list: MonsterCount, 
                reward: QuestReward, penalty: QuestPenalty) -> None:
        """
        Initialize a new quest.

        Args:
            name: The name of the quest
            description: A description of the quest objectives
            monster_list: Dictionary mapping monster names to required kill counts
            reward: Item reward for completing the quest
            penalty: Tuple of (target, value) representing the penalty for failure
        """
        self.name: str = name
        self.reward: QuestReward = reward
        self.penalty: QuestPenalty = penalty
        self.description: str = description
        self.monster_list: MonsterCount = monster_list
        self.monsters_slain: MonsterCount = {}
        for key in monster_list:
            self.monsters_slain[key] = 0

    def get_monster(self) -> Optional[Monster]:
        """
        Returns a monster that still needs to be defeated for this quest.

        Returns:
            A new monster instance if monsters remain, None if quest is complete
        """
        living_monsters: List[str] = []
        for monster_type, required_count in self.monster_list.items():
            current_count = self.monsters_slain.get(monster_type, 0)
            if current_count < required_count:
                living_monsters.append(monster_type)
        
        if living_monsters:
            return get_monster(random.choice(living_monsters))
        return None

    def slay_monster(self, monster: Monster) -> None:
        """
        Record a monster as slain for this quest.

        Args:
            monster: The monster that was slain
        """
        if monster.name in self.monsters_slain.keys():
            self.monsters_slain[monster.name] += 1

    def is_complete(self) -> bool:
        """
        Check if all required monsters have been slain.

        Returns:
            True if all monster requirements are met, False otherwise
        """
        for key in self.monster_list.keys():
            if self.monsters_slain[key] < self.monster_list[key]:
                return False
        return True
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font, 
            button: Button) -> None:
        """
        Draw the quest information on the given surface.

        Args:
            surface: Pygame surface to draw on
            font: Font to use for text
            button: Button object defining the drawing area
        """
        button.draw(surface, False, Colors.GOLD)
        draw_text(self.name, font, Colors.BLACK, surface, 
                button.pos[0] + 10, button.pos[1] + 10)
        draw_wrapped_text(self.description, font, Colors.BLACK, surface, 
                         button.pos[0] + button.size[0] // 4, 
                         button.pos[1] + 10, button.size[0] // 2 - 20)
        
        output_text = ""
        for key in self.monster_list.keys():
            output_text += f"{key}: {self.monsters_slain[key]}/{self.monster_list[key]}\n"

        draw_multiple_lines(output_text, font, Colors.BLACK, surface, 
                            button.pos[0] + button.size[0] // 4 * 3, 
                            button.pos[1] + 10)

class QuestButton(Button):
    """A button that displays quest information and tracks completion state."""

    def __init__(self, button_sheet: SpriteSheet, x: int, y: int, 
                width: int, height: int, scale: float, quest: Quest) -> None:
        """
        Initialize a new quest button.

        Args:
            button_sheet: Spritesheet containing button graphics
            x: X coordinate of the button
            y: Y coordinate of the button
            width: Width of the button
            height: Height of the button
            scale: Scale factor for the button
            quest: Quest to display on this button
        """
        super().__init__(button_sheet, x, y, width, height, scale)
        self.quest: Quest = quest
        self.selected: bool = False
        self.failed: bool = False
        if self.quest.is_complete():
            self.toggle()  # Set to selected state if quest is complete

    def mark_as_failed(self) -> None:
        """Mark the quest as failed and lock it."""
        self.failed = True
        self.lock()  # Lock the button when failed

    def draw(self, surface: Optional[pygame.Surface]) -> None:
        """
        Draw the button if a surface is provided, otherwise just update state.

        Args:
            surface: Optional pygame surface to draw on
        """
        # Check if quest completion state changed
        if self.quest.is_complete() and not self.is_toggled():
            self.toggle()
        
        self.update_state()
        
        if surface is not None:
            # Draw the base button
            image = self.button_sheet.get_image(self.state, self.width, 
                                                self.height, self.scale, Colors.BLACK)
            surface.blit(image, (self.rect.x, self.rect.y))
            
            # Draw quest information
            name_color = Colors.RED if self.failed else Colors.BLACK
            draw_text(self.quest.name, pygame.font.Font(None, 24), name_color, 
                        surface, self.rect.x + 10, self.rect.y + 10)
            
            # Draw reward/penalty with appropriate colors
            reward_color = Colors.GRAY if self.failed else Colors.GREEN
            penalty_color = Colors.GRAY if self.failed else Colors.RED
            draw_text(self.quest.reward.name, pygame.font.Font(None, 24), 
                        reward_color, surface, self.rect.x + 10, self.rect.y + 40)
            draw_text(str(self.quest.penalty), pygame.font.Font(None, 24), 
                        penalty_color, surface, self.rect.x + 10, self.rect.y + 70)

            # Draw description and progress with appropriate color
            desc_color = Colors.GRAY if self.failed else Colors.BLACK
            draw_wrapped_text(self.quest.description, pygame.font.Font(None, 24), 
                            desc_color, surface, 
                            self.rect.x + self.rect.width // 3, 
                            self.rect.y + 10, self.rect.width // 3 + 50)

            # Draw progress with appropriate color
            progress_color = Colors.GRAY if self.failed else Colors.BLACK
            output_text = ""
            for key in self.quest.monster_list.keys():
                output_text += f"{key}: {self.quest.monsters_slain[key]}/{self.quest.monster_list[key]}\n"

            draw_multiple_lines(output_text, pygame.font.Font(None, 24), 
                                progress_color, surface, 
                                self.rect.x + self.rect.width // 4 * 3 + 25, 
                                self.rect.y + 10)

            # If failed, draw "FAILED" text overlay
            if self.failed:
                failed_font = pygame.font.Font(None, 48)  # Larger font for FAILED text
                failed_text = failed_font.render("FAILED", True, Colors.RED)
                failed_rect = failed_text.get_rect()
                # Position the text in the center-right of the button
                failed_rect.center = (self.rect.centerx + self.rect.width // 4, 
                                    self.rect.centery)
                surface.blit(failed_text, failed_rect)

# Type hint for the quest list
quest_list: Set[Quest] = {
    # Quest 1
    Quest("Village Under Siege", 
        "Defend the villagers by eliminating four goblins and two orcs.", 
        {"Goblin": 4, "Orc": 2}, 
        potion_dictionary["Block Potion"], 
        ("village", -10)),
    # Quest 2
    Quest("Goblin Infestation", 
        "A horde of goblins threatens the farms! Defeat six goblins to secure the land.", 
        {"Goblin": 6}, 
        potion_dictionary["Health Potion"], 
        ("village", -10)),
    # Quest 3
    Quest("Ogre Troubles", 
        "Ogres have taken control of the mines. Slay three to reclaim the tunnels!", 
        {"Ogre": 3}, 
        potion_dictionary["Damage Potion"], 
        ("village", -10)),
    # Quest 4
Quest("Bridge of Peril", 
        "A goblin warband and their ogre leader guard the bridge. Eliminate them and restore safe passage.", 
        {"Goblin": 3, "Ogre": 1}, 
        potion_dictionary["Block Potion"], 
        ("village", -10)),
    # Quest 5
    Quest("The Forest Menace", 
        "Patrol the woods and eliminate five goblins and their ogre brute.", 
        {"Goblin": 5, "Ogre": 1}, 
        potion_dictionary["Health Potion"], 
        ("village", -10)),
    # Quest 6
    Quest("Guardian of the Ruins", 
        "The ruins hold secrets, but goblins and ogres stand in your way. Defeat them!", 
        {"Goblin": 2, "Ogre": 2}, 
        potion_dictionary["Damage Potion"], 
        ("village", -10)),
    # Quest 7
    Quest("Rampaging Goblins", 
        "A large group of goblins terrorizes the countryside. Take down seven!", 
        {"Goblin": 7}, 
        potion_dictionary["Block Potion"], 
        ("village", -10)),
    # Quest 8
    Quest("Cave Dweller's Wrath", 
        "Deep in the caves, ogres and goblins lurk. Destroy two goblins and four ogres.", 
        {"Goblin": 2, "Ogre": 4}, 
        potion_dictionary["Damage Potion"], 
        ("village", -10)),
    # Quest 9
    Quest("Battle at Dawn", 
        "A mixed force of goblins, ogres, and orcs is preparing for an assault. Strike first!", 
        {"Goblin": 3, "Ogre": 2, "Orc": 2}, 
        potion_dictionary["Block Potion"], 
        ("village", -10)),
    # Quest 10
    Quest("End of the Horde", 
        "Wipe out the remaining goblin forces, their ogre champions, and the orc warlord!", 
        {"Goblin": 6, "Ogre": 3, "Orc": 1}, 
        potion_dictionary["Health Potion"], 
        ("village", -10)),
}
