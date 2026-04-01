import pygame
import random
import math

pygame.init()

# =========================
# CONFIG
# =========================
WIDTH, HEIGHT = 21, 21
CELL = 28

SCREEN_W = WIDTH * CELL
SCREEN_H = HEIGHT * CELL

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Maze Game - Visual Edition")

clock = pygame.time.Clock()

# =========================
# COLORES (MODERNO)
# =========================
BG = (18, 18, 24)
WALL = (35, 35, 45)
WALL_SHADOW = (25, 25, 35)
PATH = (235, 235, 245)
GRID = (210, 210, 220)
PLAYER = (80, 200, 255)
EXIT = (0, 255, 140)

# =========================
# LABERINTO
# =========================
maze = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]

def generate_maze(x, y):
    maze[y][x] = 0
    dirs = [(0, -2), (0, 2), (-2, 0), (2, 0)]
    random.shuffle(dirs)

    for dx, dy in dirs:
        nx, ny = x + dx, y + dy

        if 0 < nx < WIDTH - 1 and 0 < ny < HEIGHT - 1:
            if maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                generate_maze(nx, ny)

generate_maze(1, 1)

player_x, player_y = 1, 1

def create_exit():
    for x in range(WIDTH - 2, 0, -1):
        if maze[HEIGHT - 2][x] == 0:
            return x, HEIGHT - 2
    return WIDTH - 2, HEIGHT - 2

exit_x, exit_y = create_exit()

# =========================
# TIMER
# =========================
font = pygame.font.SysFont("Arial", 22)
start_time = pygame.time.get_ticks()
end_time = None

# =========================
# MOVIMIENTO
# =========================
def move(dx, dy):
    global player_x, player_y

    nx, ny = player_x + dx, player_y + dy

    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
        if maze[ny][nx] == 0:
            player_x, player_y = nx, ny

# =========================
# DRAW MEJORADO
# =========================
def draw():
    screen.fill(BG)

    # GRID + MAZE
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)

            # pared con sombra
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WALL_SHADOW, rect.inflate(-4, -4))
                pygame.draw.rect(screen, WALL, rect.inflate(-2, -2), border_radius=4)

            # camino
            else:
                pygame.draw.rect(screen, PATH, rect)

            # grid suave
            pygame.draw.rect(screen, GRID, rect, 1)

    # =========================
    # EXIT (PULSANTE)
    # =========================
    pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5
    exit_size = int(CELL * (0.6 + pulse * 0.2))

    ex = exit_x * CELL + CELL // 2
    ey = exit_y * CELL + CELL // 2

    pygame.draw.circle(screen, EXIT, (ex, ey), exit_size // 2)

    # =========================
    # PLAYER (GLOW)
    # =========================
    px = player_x * CELL + CELL // 2
    py = player_y * CELL + CELL // 2

    # glow externo
    pygame.draw.circle(screen, (80, 200, 255, 50), (px, py), CELL // 2 + 8)
    pygame.draw.circle(screen, PLAYER, (px, py), CELL // 3)

    # =========================
    # TIMER
    # =========================
    if end_time is None:
        elapsed = (pygame.time.get_ticks() - start_time) // 1000
    else:
        elapsed = (end_time - start_time) // 1000

    text = font.render(f"Time: {elapsed}s", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # WIN TEXT
    if end_time is not None:
        win = font.render("YOU WIN!", True, EXIT)
        screen.blit(win, (SCREEN_W // 2 - 60, SCREEN_H // 2))

# =========================
# GAME LOOP
# =========================
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(0, -1)
            if event.key == pygame.K_DOWN:
                move(0, 1)
            if event.key == pygame.K_LEFT:
                move(-1, 0)
            if event.key == pygame.K_RIGHT:
                move(1, 0)

    # win condition
    if (player_x, player_y) == (exit_x, exit_y):
        if end_time is None:
            end_time = pygame.time.get_ticks()

    draw()
    pygame.display.flip()

pygame.quit()