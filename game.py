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
pygame.display.set_caption("Maze Game - Enemies")

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
ENEMY = (255, 80, 80)

# =========================
# GAME STATES
# =========================
MENU = "MENU"
PLAYING = "PLAYING"
WIN = "WIN"
LOSE = "LOSE"

game_state = MENU

# =========================
# MAZE GENERATION
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

# =========================
# VARIABLES
# =========================
maze, (exit_x, exit_y) = new_maze()
player_x, player_y = 1, 1
enemies = []

start_time = 0
end_time = 0

# =========================
# ENEMIES
# =========================
def spawn_enemies(n=3):
    global enemies
    enemies = []

    for _ in range(n):
        while True:
            x = random.randint(1, WIDTH-2)
            y = random.randint(1, HEIGHT-2)

            if maze[y][x] == 0 and (x, y) != (player_x, player_y):
                enemies.append([x, y])
                break

def move_enemies():
    for enemy in enemies:
        ex, ey = enemy

        dx = player_x - ex
        dy = player_y - ey

        moves = []

        if dx > 0: moves.append((1, 0))
        if dx < 0: moves.append((-1, 0))
        if dy > 0: moves.append((0, 1))
        if dy < 0: moves.append((0, -1))

        random.shuffle(moves)

        moved = False

        for mx, my in moves:
            nx, ny = ex + mx, ey + my
            if maze[ny][nx] == 0:
                enemy[0], enemy[1] = nx, ny
                moved = True
                break

        if not moved:
            rand_moves = [(0,1),(0,-1),(1,0),(-1,0)]
            random.shuffle(rand_moves)

            for mx, my in rand_moves:
                nx, ny = ex + mx, ey + my
                if maze[ny][nx] == 0:
                    enemy[0], enemy[1] = nx, ny
                    break

def check_collision():
    for ex, ey in enemies:
        if (ex, ey) == (player_x, player_y):
            return True
    return False

# =========================
# RESET
# =========================
def reset_game():
    global maze, exit_x, exit_y
    global player_x, player_y
    global start_time, end_time, game_state

    maze, (exit_x, exit_y) = new_maze()
    player_x, player_y = 1, 1

    spawn_enemies(3)

    start_time = pygame.time.get_ticks()
    end_time = 0

    game_state = PLAYING

# =========================
# MOVEMENT
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

    # EXIT (pulse)
    pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5
    size = int(CELL * (0.6 + pulse * 0.2))

    ex = exit_x * CELL + CELL // 2
    ey = exit_y * CELL + CELL // 2
    pygame.draw.circle(screen, EXIT, (ex, ey), size // 2)

    # PLAYER
    px = player_x * CELL + CELL // 2
    py = player_y * CELL + CELL // 2
    pygame.draw.circle(screen, PLAYER, (px, py), CELL // 3)

    # ENEMIES
    for ex, ey in enemies:
        ex_pos = ex * CELL + CELL // 2
        ey_pos = ey * CELL + CELL // 2
        pygame.draw.circle(screen, ENEMY, (ex_pos, ey_pos), CELL // 3)

    # TIMER
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
# DRAW LOSE
# =========================
def draw_lose():
    screen.fill(BG)
    text = font.render("GAME OVER", True, ENEMY)
    restart = font.render("Press R to Retry", True, (255, 255, 255))

    screen.blit(text, (WIDTH*CELL//2 - 80, HEIGHT*CELL//2 - 30))
    screen.blit(restart, (WIDTH*CELL//2 - 110, HEIGHT*CELL//2))

# =========================
# MAIN LOOP
# =========================
running = True

while running:
    clock.tick(8)  # enemigos más lentos

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

            elif game_state in [WIN, LOSE]:
                if event.key == pygame.K_r:
                    game_state = MENU

    # GAME LOGIC
    if game_state == PLAYING:
        move_enemies()

        if check_collision():
            game_state = LOSE

        if (player_x, player_y) == (exit_x, exit_y):
            game_state = WIN

    # DRAW
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        draw_game()
    elif game_state == WIN:
        draw_win()
    elif game_state == LOSE:
        draw_lose()

    pygame.display.flip()

pygame.quit()