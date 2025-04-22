class PauseManager:
    def __init__(self):
        self.paused = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def toggle(self):
        self.paused = not self.paused

    def is_paused(self):
        return self.paused