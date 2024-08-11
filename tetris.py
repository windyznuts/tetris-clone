import pygame
import random

pygame.init()


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]],  # J shape
]


#the base functions 

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

def check_collision(grid, shape, pos):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if (y + pos[0] >= GRID_HEIGHT or
                    x + pos[1] < 0 or
                    x + pos[1] >= GRID_WIDTH or
                    grid[y + pos[0]][x + pos[1]]):
                    return True
    return False

def clear_lines(grid):
    lines_cleared = 0
    for i, row in enumerate(grid):
        if all(row):
            del grid[i]
            grid.insert(0, [0] * GRID_WIDTH)
            lines_cleared += 1
    return lines_cleared

def check_game_over(grid):
    return any(grid[0])

def update_score(lines_cleared):
    return lines_cleared * 100


def main():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()


    
    # Initialize grid and game state
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_shape = random.choice(SHAPES)
    shape_pos = [0, GRID_WIDTH // 2 - len(current_shape[0]) // 2]
    score = 0
    running = True

    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(grid, current_shape, (shape_pos[0], shape_pos[1] - 1)):
                        shape_pos[1] -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(grid, current_shape, (shape_pos[0], shape_pos[1] + 1)):
                        shape_pos[1] += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(grid, current_shape, (shape_pos[0] + 1, shape_pos[1])):
                        shape_pos[0] += 1
                elif event.key == pygame.K_UP:
                    rotated_shape = rotate_shape(current_shape)
                    if not check_collision(grid, rotated_shape, shape_pos):
                        current_shape = rotated_shape

        # Move the shape down automatically
        if not check_collision(grid, current_shape, (shape_pos[0] + 1, shape_pos[1])):
            shape_pos[0] += 1
        else:
            for y, row in enumerate(current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[y + shape_pos[0]][x + shape_pos[1]] = 1
            lines_cleared = clear_lines(grid)
            score += update_score(lines_cleared)
            current_shape = random.choice(SHAPES)
            shape_pos = [0, GRID_WIDTH // 2 - len(current_shape[0]) // 2]
            if check_game_over(grid):
                running = False
                print("Game Over! Your score:", score)

        # Draw the grid and current shape
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x]:
                    pygame.draw.rect(screen, BLUE, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        for y, row in enumerate(current_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, RED, pygame.Rect((shape_pos[1] + x) * GRID_SIZE, (shape_pos[0] + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
