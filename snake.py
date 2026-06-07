import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
BLOCK = 20

import os
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

background = pygame.image.load(
    resource_path("background.png")
)

background = pygame.transform.scale(background, (WIDTH, HEIGHT))

menu_background = pygame.image.load(
    resource_path("menu_background.png")
)

menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

apple_img = pygame.image.load(
    resource_path("apple.png")
)

apple_img = pygame.transform.scale(
    apple_img,
    (BLOCK, BLOCK)
)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (0, 150, 255)
DARK_GREEN = (0, 80, 200)
RED = (255, 60, 60)
YELLOW = (255, 220, 0)

title_font = pygame.font.Font(
    resource_path("Pixel Game.otf"), 72
)

font = pygame.font.Font(
    resource_path("Pixel Game.otf"), 48
)

highest_score = 0


def draw_text(text, font_obj, color, x, y):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))


def random_food():
    return (
        random.randrange(0, WIDTH // BLOCK) * BLOCK,
        random.randrange(0, HEIGHT // BLOCK) * BLOCK
    )


def menu():
    while True:
        screen.blit(menu_background, (0, 0))

        draw_text("SNAKE GAME", title_font, GREEN, 260, 120)

        draw_text("ENTER - Play", font, RED, 300, 320)
        draw_text("ESC - Exit", font, RED, 320, 370)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    return

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def game_over_screen(score):
    global highest_score

    if score > highest_score:
        highest_score = score

    while True:

        screen.blit(background, (0, 0))

        draw_text("GAME OVER", title_font, RED, 270, 120)

        draw_text(f"Score:{score}", font, WHITE, 330, 250)
        draw_text(f"Highest Score:{highest_score}",
                  font, YELLOW, 260, 300)

        draw_text("R - Play Again", font, GREEN, 280, 350)
        draw_text("ESC - Exit", font, WHITE, 320, 400)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    return True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def game():

    snake = [(200, 200)]
    direction = (BLOCK, 0)

    food = random_food()

    score = 0
    speed = 10

    running = True

    while running:

        clock.tick(speed)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP and direction != (0, BLOCK):
                    direction = (0, -BLOCK)

                elif event.key == pygame.K_DOWN and direction != (0, -BLOCK):
                    direction = (0, BLOCK)

                elif event.key == pygame.K_LEFT and direction != (BLOCK, 0):
                    direction = (-BLOCK, 0)

                elif event.key == pygame.K_RIGHT and direction != (-BLOCK, 0):
                    direction = (BLOCK, 0)

        head_x = snake[0][0] + direction[0]
        head_y = snake[0][1] + direction[1]

        new_head = (head_x, head_y)

        # Đâm tường
        if (
            head_x < 0 or
            head_x >= WIDTH or
            head_y < 0 or
            head_y >= HEIGHT
        ):
            return score

        # Cắn thân
        if new_head in snake:
            return score

        snake.insert(0, new_head)

        # Ăn thức ăn
        if new_head == food:

            score += 10

            speed = min(30, 10 + score // 20)

            while True:
                food = random_food()

                if food not in snake:
                    break

        else:
            snake.pop()

        # Vẽ
        screen.blit(background, (0, 0))

        # Thức ăn
        screen.blit(apple_img, (food[0], food[1]))

        # Rắn
        for i, segment in enumerate(snake):

            color = GREEN if i == 0 else DARK_GREEN

            pygame.draw.rect(
                screen,
                color,
                (segment[0], segment[1], BLOCK, BLOCK)
            )

        draw_text(f"Score:{score}",
                  font,
                  WHITE,
                  10,
                  10)

        draw_text(f"Highest:{highest_score}",
                  font,
                  YELLOW,
                  600,
                  10)

        pygame.display.flip()


def main():

    while True:

        menu()

        score = game()

        play_again = game_over_screen(score)

        if not play_again:
            break


main()