import pygame
import random
import math

pygame.init()

# =========================
# CONFIG
# =========================
WIDTH, HEIGHT = 21, 21
CELL = 28

screen = pygame.display.set_mode((WIDTH * CELL, HEIGHT * CELL))
pygame.display.set_caption("Maze Game - Pro Version")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

# =========================
# COLORS
# =========================
BG = (18, 18, 24)
WALL = (35, 35, 45)
WALL_SHADOW = (25, 25, 35)
PATH = (235, 235, 245)
GRID = (210, 210, 220)
PLAYER = (80, 200, 255)
EXIT = (0, 255, 140)

# =========================
# GAME STATE
# =========================
MENU = "MENU"
PLAYING = "PLAYING"
WIN = "WIN"

game_state = MENU

# =========================
# MAZE
# =========================
def new_maze():
    maze = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def generate(x, y):
        maze[y][x] = 0
        dirs = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(dirs)

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 < nx < WIDTH - 1 and 0 < ny < HEIGHT - 1:
                if maze[ny][nx] == 1:
                    maze[y + dy // 2][x + dx // 2] = 0
                    generate(nx, ny)

    generate(1, 1)

    def create_exit():
        for x in range(WIDTH - 2, 0, -1):
            if maze[HEIGHT - 2][x] == 0:
                return x, HEIGHT - 2
        return WIDTH - 2, HEIGHT - 2

    return maze, create_exit()

maze, (exit_x, exit_y) = new_maze()

player_x, player_y = 1, 1

start_time = 0
end_time = 0

# =========================
# RESET
# =========================
def reset_game():
    global maze, exit_x, exit_y
    global player_x, player_y, start_time, end_time, game_state

    maze, (exit_x, exit_y) = new_maze()
    player_x, player_y = 1, 1

    start_time = pygame.time.get_ticks()
    end_time = 0

    game_state = PLAYING

# =========================
# MOVE
# =========================
def move(dx, dy):
    global player_x, player_y

    nx, ny = player_x + dx, player_y + dy

    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
        if maze[ny][nx] == 0:
            player_x, player_y = nx, ny

# =========================
# DRAW MENU
# =========================
def draw_menu():
    screen.fill(BG)
    title = font.render("MAZE GAME", True, (255, 255, 255))
    start = font.render("Press ENTER to Start", True, EXIT)

    screen.blit(title, (WIDTH*CELL//2 - 60, HEIGHT*CELL//2 - 40))
    screen.blit(start, (WIDTH*CELL//2 - 130, HEIGHT*CELL//2))

# =========================
# DRAW GAME
# =========================
def draw_game():
    screen.fill(BG)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)

            if maze[y][x] == 1:
                pygame.draw.rect(screen, WALL_SHADOW, rect.inflate(-4, -4))
                pygame.draw.rect(screen, WALL, rect.inflate(-2, -2), border_radius=4)
            else:
                pygame.draw.rect(screen, PATH, rect)

            pygame.draw.rect(screen, GRID, rect, 1)

    # exit pulse
    pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5
    size = int(CELL * (0.6 + pulse * 0.2))

    ex = exit_x * CELL + CELL // 2
    ey = exit_y * CELL + CELL // 2
    pygame.draw.circle(screen, EXIT, (ex, ey), size // 2)

    # player
    px = player_x * CELL + CELL // 2
    py = player_y * CELL + CELL // 2
    pygame.draw.circle(screen, PLAYER, (px, py), CELL // 3)

    # timer
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    text = font.render(f"Time: {elapsed}s", True, (255, 255, 255))
    screen.blit(text, (10, 10))

# =========================
# DRAW WIN
# =========================
def draw_win():
    screen.fill(BG)
    text = font.render("YOU WIN!", True, EXIT)
    restart = font.render("Press R to Restart", True, (255, 255, 255))

    screen.blit(text, (WIDTH*CELL//2 - 60, HEIGHT*CELL//2 - 30))
    screen.blit(restart, (WIDTH*CELL//2 - 120, HEIGHT*CELL//2))

# =========================
# LOOP
# =========================
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == MENU:
                if event.key == pygame.K_RETURN:
                    reset_game()

            elif game_state == PLAYING:
                if event.key == pygame.K_UP:
                    move(0, -1)
                if event.key == pygame.K_DOWN:
                    move(0, 1)
                if event.key == pygame.K_LEFT:
                    move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    move(1, 0)

            elif game_state == WIN:
                if event.key == pygame.K_r:
                    game_state = MENU

    # WIN CONDITION
    if game_state == PLAYING:
        if (player_x, player_y) == (exit_x, exit_y):
            game_state = WIN

    # RENDER
    if game_state == MENU:
        draw_menu()

    elif game_state == PLAYING:
        draw_game()

    elif game_state == WIN:
        draw_win()

    pygame.display.flip()

pygame.quit()