import pygame
import random
import sys

pygame.init()

# =====================
# KONFIGURASI
# =====================
WIDTH, HEIGHT = 400, 400
BLOCK = 20
FPS = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Level Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 18)
big_font = pygame.font.SysFont("arial", 32)

# =====================
# FUNGSI
# =====================
def draw_text(text, font, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

def draw_button(rect, text):
    pygame.draw.rect(screen, (50, 50, 50), rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
    txt = font.render(text, True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect.center))

def reset_snake():
    return [(200, 200)], (BLOCK, 0)

# =====================
# GAME VAR
# =====================
snake, direction = reset_snake()
next_direction = direction

food = (random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK))

score = 0
level = 1
eaten = 0
target = 4
lives = 3

snake_delay = 150
last_move = pygame.time.get_ticks()

paused = True
overlay = "PLAY"   # PLAY | NEXT | GAMEOVER | READY

# =====================
# BUTTON RECT
# =====================
btn_play  = pygame.Rect(130, 180, 140, 30)
btn_next  = pygame.Rect(130, 180, 140, 30)
btn_retry = pygame.Rect(130, 220, 140, 30)
btn_gover = pygame.Rect(130, 190, 140, 30)

# =====================
# GAME LOOP
# =====================
running = True
while running:
    clock.tick(FPS)
    now = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # =====================
        # MOUSE CLICK
        # =====================
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if paused:
                if overlay == "PLAY" and btn_play.collidepoint(mouse_pos):
                    paused = False

                elif overlay == "READY" and btn_play.collidepoint(mouse_pos):
                    paused = False

                elif overlay == "NEXT":
                    if btn_next.collidepoint(mouse_pos):
                        paused = False
                    elif btn_retry.collidepoint(mouse_pos):
                        snake, direction = reset_snake()
                        next_direction = direction
                        eaten = 0
                        paused = False

                elif overlay == "GAMEOVER" and btn_gover.collidepoint(mouse_pos):
                    snake, direction = reset_snake()
                    next_direction = direction
                    score = 0
                    level = 1
                    eaten = 0
                    target = 4
                    lives = 3
                    paused = True
                    overlay = "PLAY"

        # =====================
        # KEYBOARD (TETAP ADA)
        # =====================
        if event.type == pygame.KEYDOWN:

            if not paused:
                if event.key == pygame.K_UP and direction != (0, BLOCK):
                    next_direction = (0, -BLOCK)
                elif event.key == pygame.K_DOWN and direction != (0, -BLOCK):
                    next_direction = (0, BLOCK)
                elif event.key == pygame.K_LEFT and direction != (BLOCK, 0):
                    next_direction = (-BLOCK, 0)
                elif event.key == pygame.K_RIGHT and direction != (-BLOCK, 0):
                    next_direction = (BLOCK, 0)

            if paused:
                if overlay in ["PLAY", "READY"] and event.key == pygame.K_RETURN:
                    paused = False
                elif overlay == "NEXT" and event.key == pygame.K_n:
                    paused = False
                elif overlay == "GAMEOVER" and event.key == pygame.K_r:
                    snake, direction = reset_snake()
                    next_direction = direction
                    score = 0
                    level = 1
                    eaten = 0
                    target = 4
                    lives = 3
                    paused = True
                    overlay = "PLAY"

    # =====================
    # GERAK SNAKE
    # =====================
    if not paused and now - last_move > snake_delay:
        last_move = now
        direction = next_direction

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)

        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            lives -= 1
            snake, direction = reset_snake()
            next_direction = direction
            paused = True
            overlay = "READY"
            if lives == 0:
                overlay = "GAMEOVER"

        if head == food:
            score += 10
            eaten += 1
            food = (random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK))
        else:
            snake.pop()

        if eaten >= target:
            level += 1
            eaten = 0
            target += 1
            snake_delay = max(60, snake_delay - 15)
            paused = True
            overlay = "NEXT"

    # =====================
    # RENDER
    # =====================
    screen.fill((0, 0, 0))

    draw_text(f"Score: {score}", font, (255,255,255), 10, 5)
    draw_text(f"Level: {level}", font, (255,255,0), 120, 5)
    draw_text(f"Lives: {lives}", font, (255,100,100), 300, 5)

    for part in snake:
        pygame.draw.rect(screen, (0,255,0), (*part, BLOCK, BLOCK))
    pygame.draw.rect(screen, (255,0,0), (*food, BLOCK, BLOCK))

    # =====================
    # OVERLAY + BUTTON
    # =====================
    if paused:
        pygame.draw.rect(screen, (0,0,0), (80,130,240,150))
        pygame.draw.rect(screen, (255,255,255), (80,130,240,150), 2)

        if overlay == "PLAY":
            draw_text("PLAY", big_font, (0,255,0), 150, 145)
            draw_button(btn_play, "START")

        elif overlay == "READY":
            draw_text("READY?", big_font, (255,255,0), 130, 145)
            draw_button(btn_play, "CONTINUE")

        elif overlay == "NEXT":
            draw_text("LEVEL COMPLETE", font, (0,255,255), 115, 140)
            draw_button(btn_next, "NEXT LEVEL")
            draw_button(btn_retry, "RESTART")

        elif overlay == "GAMEOVER":
            draw_text("GAME OVER", big_font, (255,0,0), 110, 145)
            draw_button(btn_gover, "RESTART GAME")

    pygame.display.flip()

pygame.quit()
sys.exit()
