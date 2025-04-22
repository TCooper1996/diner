from dataclasses import dataclass
import pygame
import pygame_gui

from src.tui.gui.ui_manager import UIManager
@dataclass
class WidgetDimensions:
    width: int
    height: int

def make_gui(width, height) -> UIManager:
    manager = pygame_gui.UIManager((width, height))
    turn_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20, 20), (100, 50)),
                                            text='Say Hello',
                                            manager=manager)
    pause_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20, 80), (100, 50)),
                                            text='Paused',
                                            manager=manager)
    message_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((20, 140), (300, 200)),
                                                html_text='No messages',
                                                manager=manager)
    _manager = UIManager(manager, turn_label, pause_label, message_box)

    return _manager