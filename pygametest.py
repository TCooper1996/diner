import pygame
import sys
import random
import os

# === Configuration ===
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CELL_SIZE = 64
GRID_COLS = SCREEN_WIDTH // CELL_SIZE
GRID_ROWS = SCREEN_HEIGHT // CELL_SIZE

# === Initialize Pygame ===
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Emoji Grid Prototype (Image-Based)")



def emoji_to_twemoji_filename(emoji):
    """
    Converts an emoji string to a filename used in Twemoji assets.
    For example, '😀' becomes '1f600.png' and
    '👨‍👩‍👧‍👦' becomes '1f468-200d-1f469-200d-1f467-200d-1f466.png'
    """
    return "-".join("{:x}".format(ord(c)) for c in emoji) + ".svg"

# === Emoji Image Provider ===
# This class is our abstraction for loading emoji images.
# Later you can swap out its implementation (e.g. using Pillow or an emoji sheet)
class EmojiImageProvider:
    def __init__(self, images_path="/Users/taylercooper/Dev/openmoji-svg-color", default_size=(CELL_SIZE, CELL_SIZE)):
        self.images_path = images_path
        self.default_size = default_size
        self.cache = {}
        # Mapping from emoji character to image filename.
        # Update these filenames to match the actual images in your emoji_images folder.
    
    def get_image(self, emoji):
        # Return cached image if available.
        if emoji in self.cache:
            return self.cache[emoji]
        filename = emoji_to_twemoji_filename(emoji)
        
        full_path = os.path.join(self.images_path, filename)
        image =pygame.image.load(full_path).convert_alpha()
        # Scale the image to the default cell size.
        image = pygame.transform.smoothscale(image, self.default_size)
        self.cache[emoji] = image
        return image

# Instantiate the provider.
emoji_provider = EmojiImageProvider()

# === Sample Emoji List ===
# Use emojis that match keys in the provider's mapping.
emoji_list = [
    "😀", "👩", "👨", "🧑", "👻", "🎃", "🐱", "🐶",
    "🦊", "💀", "👨‍👩‍👧‍👦", "👩‍❤️‍👨", "🧙‍♂️"
]

# === Build a Random Grid ===
grid = []
for row in range(GRID_ROWS):
    grid_row = []
    for col in range(GRID_COLS):
        num_emojis = random.choice([0, 1, 2, 3, 4])
        if num_emojis == 0:
            cell_emojis = []
        else:
            # Randomly choose a sample of emojis for this cell.
            cell_emojis = random.sample(emoji_list, num_emojis)
        grid_row.append(cell_emojis)
    grid.append(grid_row)

# === Drawing Function ===
def draw_tile(x, y, emojis):
    cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    # Draw cell border.
    pygame.draw.rect(screen, (50, 50, 50), cell_rect, 1)
    
    if not emojis:
        return

    if len(emojis) == 1:
        # Draw single emoji image centered in the cell.
        img = emoji_provider.get_image(emojis[0])
        img_rect = img.get_rect(center=cell_rect.center)
        screen.blit(img, img_rect)
    else:
        # For multiple emojis, divide the cell into quadrants.
        quadrant_width = CELL_SIZE // 2
        quadrant_height = CELL_SIZE // 2
        positions = [
            (x, y),  # top-left
            (x + quadrant_width, y),  # top-right
            (x, y + quadrant_height),  # bottom-left
            (x + quadrant_width, y + quadrant_height)  # bottom-right
        ]
        for i, emoji in enumerate(emojis[:4]):
            # Get the full-size image.
            img = emoji_provider.get_image(emoji)
            # Scale it to fit in the quadrant.
            quad_img = pygame.transform.smoothscale(img, (quadrant_width, quadrant_height))
            quad_rect = quad_img.get_rect(center=(positions[i][0] + quadrant_width // 2,
                                                   positions[i][1] + quadrant_height // 2))
            screen.blit(quad_img, quad_rect)

# === Main Game Loop ===
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            draw_tile(x, y, grid[row][col])
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()