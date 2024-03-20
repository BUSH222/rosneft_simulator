import pygame
import sys
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
    cnt = 0
    grid = helper.TileGrid(10, 10)
    coords1 = [0, 0]
    coords2 = [0, 0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    tile_x, tile_y = get_tile_coordinates(pygame.mouse.get_pos())
                    coords1 = [tile_x, tile_y]
                elif event.button == 3:
                    tile_x, tile_y = get_tile_coordinates(pygame.mouse.get_pos())
                    coords3 = [tile_x, tile_y]

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    tile_x, tile_y = get_tile_coordinates(pygame.mouse.get_pos())
                    coords2 = [tile_x, tile_y]
                    print(coords2)
                    grid.place_pipes(coords1[1], coords1[0], coords2[1], coords2[0], preview=False)
                if event.button == 3:
                    tile_x, tile_y = get_tile_coordinates(pygame.mouse.get_pos())
                    coords4 = [tile_x, tile_y]
                    print(coords4)
                    grid.place_pipes(coords3[1], coords3[0], coords4[1], coords4[0], preview=True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.clear_previews()
                if event.key == pygame.K_0:
                    grid.validate_all()
                if event.key == pygame.K_1:
                    for s in grid.grid:
                        print(*s)
        screen.fill(WHITE)
        draw_grid()

        # Draw colored tiles
        for i, x in enumerate(grid.grid):
            for j, y in enumerate(x):
                rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, y.draw(), rect)

        if cnt % 50 == 80:  # change later, temp
            grid.validate_all()

        pygame.display.update()
        clock.tick(FPS)
        cnt += 1


if __name__ == "__main__":
    main()
