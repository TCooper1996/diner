
import pygame

from src.tui.app.intent import *


def handle_pygame_event(event: pygame.event.Event) -> AppCommand | None:
    if event.type == pygame.QUIT:
        return QuitCommand()

    elif event.type == pygame.VIDEORESIZE:
        return ResizeCommand(event.w, event.h)

    elif event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_ESCAPE:
                return QuitCommand()
            case pygame.K_r:
                return RestartCommand()
            case pygame.K_e | pygame.K_RIGHT:
                return ViewNextTickCommand()
            case pygame.K_LEFT | pygame.K_LEFT:
                return ViewPreviousTickCommand()
            case pygame.K_p:
                return PauseCommand()

    return None