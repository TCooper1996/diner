
from time import sleep, time
import pygame
from src.tui.app.get_event import all_events
from src.tui.app.window_state import WindowState
from src.tui.gui.make_gui import make_gui
from src.tui.gui.widget_layout import compute_layout


class TestWindow:
    def test_draw_window(self):
        width = 800
        height = 600
        pygame.init()
        surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        manager = make_gui(800, 600)
        surface.fill((0, 0, 0))
        state = WindowState.default()
        messages = state.focused_snapshot.turn_summaries
        snap = UpdateWindowInput([], state.paused, state.current_turn_num, state.max_turn_num, messages, state.width, state.height, state.current_entity)
        update_window(manager, surface, snap, 0.016)

        running = True
        start_time = time()
        clock = pygame.time.Clock()
        manager.message_box.set_text("\n".join(["test"]*100))
        while running and (time() - start_time) < 10:
            time_delta = clock.tick(60) / 1000
            surface.fill((0, 0, 0))
            layout = compute_layout(width, height)
            for event in pygame.event.get():
                manager.ui_manager.process_events(event)
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.VIDEORESIZE:
                    width, height = event.w, event.h
                    manager.ui_manager.set_window_resolution((width, height))
                    layout = compute_layout(width, height)
                    manager.turn_label.set_relative_position((layout.turn_rect.x, layout.turn_rect.y))
                    manager.turn_label.set_dimensions((layout.turn_rect.width, layout.turn_rect.height))
                    manager.message_box.set_relative_position((0, layout.message_rect.y))
                    manager.message_box.set_dimensions((layout.message_rect.width, layout.message_rect.height))
            manager.ui_manager.update(time_delta)
            manager.ui_manager.draw_ui(surface)
            pygame.display.flip()
                #update_window(manager, surface, update_input, 0.016)

        pygame.quit()