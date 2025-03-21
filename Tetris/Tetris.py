import pygame
import random

# Initialize Pygame
pygame.init()

# Get screen size
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
BLOCK_SIZE = SCREEN_HEIGHT // 20  # Adjust block size based on screen height
GAME_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GAME_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Define Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

# Create full-screen window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Tetris")

# Game clock
clock = pygame.time.Clock()
fall_speed = 500  # Milliseconds per move

# Draw the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

# Draw Tetromino
def draw_tetromino(tetromino, offset):
    for y, row in enumerate(tetromino):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, RED, (offset[0] * BLOCK_SIZE + x * BLOCK_SIZE, offset[1] * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Draw placed blocks
def draw_board(board):
    for y in range(GAME_HEIGHT):
        for x in range(GAME_WIDTH):
            if board[y][x]:
                pygame.draw.rect(screen, BLUE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Check if Tetromino can be placed
def valid_position(board, tetromino, offset):
    for y, row in enumerate(tetromino):
        for x, cell in enumerate(row):
            if cell:
                px = offset[0] + x
                py = offset[1] + y
                if px < 0 or px >= GAME_WIDTH or py >= GAME_HEIGHT or board[py][px]:
                    return False
    return True

# Clear full lines
def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = GAME_HEIGHT - len(new_board)
    return [[0] * GAME_WIDTH] * lines_cleared + new_board, lines_cleared

# Rotate Tetromino
def rotate(tetromino):
    return [list(reversed(col)) for col in zip(*tetromino)]

# Pause Screen with Restart Button
def pause_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, SCREEN_WIDTH // 15)
    text = font.render("Paused", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(text, text_rect)

    button_font = pygame.font.Font(None, SCREEN_WIDTH // 20)
    button_text = button_font.render("Restart", True, BLACK)
    button_rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 10)

    pygame.draw.rect(screen, WHITE, button_rect)
    screen.blit(button_text, button_text.get_rect(center=button_rect.center))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Resume game
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Restart game
                    return "restart"

# Game Over Screen
def game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, SCREEN_WIDTH // 15)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(text, text_rect)

    button_font = pygame.font.Font(None, SCREEN_WIDTH // 20)
    button_text = button_font.render("Restart", True, BLACK)
    button_rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 10)

    pygame.draw.rect(screen, WHITE, button_rect)
    screen.blit(button_text, button_text.get_rect(center=button_rect.center))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Restart game
                    return True

# Main game loop
def main():
    board = [[0] * GAME_WIDTH for _ in range(GAME_HEIGHT)]
    tetromino = random.choice(SHAPES)
    offset = [GAME_WIDTH // 2 - len(tetromino[0]) // 2, 0]
    last_fall_time = pygame.time.get_ticks()
    game_over = False
    paused = False

    while not game_over:
        screen.fill(BLACK)
        draw_grid()
        draw_board(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_offset = [offset[0] - 1, offset[1]]
                    if valid_position(board, tetromino, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_RIGHT:
                    new_offset = [offset[0] + 1, offset[1]]
                    if valid_position(board, tetromino, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_DOWN:
                    new_offset = [offset[0], offset[1] + 1]
                    if valid_position(board, tetromino, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_UP:
                    rotated = rotate(tetromino)
                    if valid_position(board, rotated, offset):
                        tetromino = rotated
                elif event.key == pygame.K_p:  # Pause game
                    action = pause_screen()
                    if action == "restart":
                        main()
                        return
                elif event.key == pygame.K_ESCAPE:  # Quit game with ESC
                    pygame.quit()
                    return

        # Auto move down
        current_time = pygame.time.get_ticks()
        if current_time - last_fall_time > fall_speed:
            last_fall_time = current_time
            new_offset = [offset[0], offset[1] + 1]
            if valid_position(board, tetromino, new_offset):
                offset = new_offset
            else:
                # Lock piece in place
                for y, row in enumerate(tetromino):
                    for x, cell in enumerate(row):
                        if cell:
                            board[offset[1] + y][offset[0] + x] = 1

                # Clear full lines
                board, _ = clear_lines(board)

                # Spawn new piece
                tetromino = random.choice(SHAPES)
                offset = [GAME_WIDTH // 2 - len(tetromino[0]) // 2, 0]

                # Check Game Over
                if not valid_position(board, tetromino, offset):
                    game_over = True

        draw_tetromino(tetromino, offset)

        pygame.display.update()
        clock.tick(30)

    if game_over_screen():
        main()

    pygame.quit()

if __name__ == "__main__":
    main()
