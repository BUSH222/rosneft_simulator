import pygame
import sys
import random
import helper

# Initialize pygame
pygame.init()

# Constants
WINDOW_SIZE = (500, 500)
TILE_SIZE = WINDOW_SIZE[0] // 10
GRID_SIZE = 10

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

clock = pygame.time.Clock()
FPS = 50

# Create the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tile Grid")

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

def get_tile_coordinates(mouse_pos):
    x, y = mouse_pos
    tile_x = x // TILE_SIZE
    tile_y = y // TILE_SIZE
    return tile_x, tile_y

def random_color():
    return (250, 250, 250)
    # return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def main():
    grid = helper.TileGrid(10, 10)


    coords1 = [0, 0]
    coords2 = [0, 0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    tile_x, tile_y = get_tile_coordinates(pygame.mouse.get_pos())
                    coords1 = [tile_x, tile_y]
                    print(coords1)
                elif event.button == 3:
                    tile_x, tile_y = get_tile_coordinates(pygame.mouse.get_pos())
                    coords2 = [tile_x, tile_y]
                    print(coords2)
                    grid.place_pipes(coords1[0], coords1[1], coords2[0], coords2[1], preview=False)

        screen.fill(WHITE)
        draw_grid()

        # Draw colored tiles
        for i, x in enumerate(grid.grid):
            for j, y in enumerate(x):
                rect = pygame.Rect(i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, y.draw(), rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()