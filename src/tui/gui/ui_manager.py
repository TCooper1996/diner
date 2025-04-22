import pygame
import pygame_gui
from pygame_gui.elements import UILabel, UITextBox

class UIManager:
    def __init__(self, ui_manager: pygame_gui.UIManager, turn_label: UILabel, pause_label: UILabel, message_box: UITextBox):
        self.ui_manager = ui_manager
        self.turn_label:UILabel = turn_label
        self.pause_label: UILabel = pause_label
        self.message_box: UITextBox = message_box

    def update(self, time_delta: float, surface):
        self.ui_manager.update(time_delta)
        self.ui_manager.draw_ui(surface)

    def process_events(self, event: pygame.event.Event):
        self.ui_manager.process_events(event)