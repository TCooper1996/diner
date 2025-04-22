
def draw_level(self):
    self.resize_images_if_necessary()
    print(f"Redrawing. CellSize: {self.CELL_SIZE}, size of entities: {self.entities[0].image.get_size() if self.entities else 'N/A'}")
    self.screen.fill((0, 0, 0))  # Clear the screen with black
    draw_level(self.screen, self.CELL_SIZE, self.entities) 
    pygame.display.flip()  # Update the display

def resize_images_if_necessary(self):
    if not self.entities:
        return
    
    for entity in self.entities:
        if entity.image.get_size() != (self.CELL_SIZE, self.CELL_SIZE):
            entity.image = pygame.transform.smoothscale(entity.image, (self.CELL_SIZE, self.CELL_SIZE))