
import pygame

from src.tui.app.intent import *


def handle_pygame_event(event: pygame.event.Event) -> AppIntent | None:
    if event.type == pygame.QUIT:
        return AppEffect(QuitEffect())

    elif event.type == pygame.VIDEORESIZE:
        return AppCommand(ResizeCommand(event.w, event.h))

    elif event.type == pygame.KEYDOWN:
        match event.key:
            case pygame.K_ESCAPE:
                return AppEffect(QuitEffect())
            case pygame.K_r:
                return AppEffect(RestartEffect())
            case pygame.K_e | pygame.K_RIGHT:
                return AppCommand(ViewNextTickCommand())
            case pygame.K_LEFT | pygame.K_LEFT:
                return AppCommand(ViewPreviousTickCommand())
            case pygame.K_p:
                return AppCommandEffect(PauseCommandEffect())

    return None