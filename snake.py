import pygame, random, sys, os

pygame.init()
WIDTH, HEIGHT, BLOCK = 800, 600, 20

def path(file):
    try: return os.path.join(sys._MEIPASS, file)
    except: return os.path.join(os.path.abspath("."), file)

class Snake:
    def __init__(self):
        self.body = [(200, 200)]
        self.dir = (BLOCK, 0)

    def move(self):
        head = (self.body[0][0] + self.dir[0], self.body[0][1] + self.dir[1])
        self.body.insert(0, head)
        return head

    def draw(self, screen):
        for i, p in enumerate(self.body):
            color = (0,150,255) if i == 0 else (0,80,200)
            pygame.draw.rect(screen, color, (*p, BLOCK, BLOCK))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.bg = pygame.transform.scale(
            pygame.image.load(path("background.png")), (WIDTH, HEIGHT))

        self.menu_bg = pygame.transform.scale(
            pygame.image.load(path("menu_background.png")), (WIDTH, HEIGHT))

        self.apple = pygame.transform.scale(
            pygame.image.load(path("apple.png")), (BLOCK, BLOCK))

        self.font = pygame.font.Font(path("Pixel Game.otf"), 40)
        self.big = pygame.font.Font(path("Pixel Game.otf"), 70)

        self.highest = 0

    def text(self, txt, x, y, color=(255,255,255), big=False):
        font = self.big if big else self.font
        self.screen.blit(font.render(txt, True, color), (x, y))

    def food(self):
        return random.randrange(WIDTH//BLOCK)*BLOCK, random.randrange(HEIGHT//BLOCK)*BLOCK

    def menu(self):
        while True:
            self.screen.blit(self.menu_bg, (0,0))
            self.text("SNAKE GAME", 20, 120, (255,60,60), True)
            self.text("ENTER - PLAY", 30, 320)
            self.text("ESC - EXIT", 30, 380)
            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN: return
                    if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

    def game_over(self, score):
        self.highest = max(self.highest, score)

        while True:
            self.screen.blit(self.bg, (0,0))
            self.text("GAME OVER", 280, 120, (255,60,60), True)
            self.text(f"Score: {score}", 350, 260)
            self.text(f"Highest: {self.highest}", 340, 320, (255,220,0))
            self.text("R - PLAY AGAIN", 320, 400)
            self.text("ESC - EXIT", 350, 460)
            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r: return
                    if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

    def play(self):
        snake = Snake()
        food = self.food()
        score, speed = 0, 10

        while True:
            self.clock.tick(speed)

            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP and snake.dir != (0,BLOCK):
                        snake.dir = (0,-BLOCK)
                    elif e.key == pygame.K_DOWN and snake.dir != (0,-BLOCK):
                        snake.dir = (0,BLOCK)
                    elif e.key == pygame.K_LEFT and snake.dir != (BLOCK,0):
                        snake.dir = (-BLOCK,0)
                    elif e.key == pygame.K_RIGHT and snake.dir != (-BLOCK,0):
                        snake.dir = (BLOCK,0)

            head = snake.move()

            if (head[0] < 0 or head[0] >= WIDTH or
                head[1] < 0 or head[1] >= HEIGHT or
                head in snake.body[1:]):
                return score

            if head == food:
                score += 10
                speed = min(30, 10 + score//20)
                while True:
                    food = self.food()
                    if food not in snake.body: break
            else:
                snake.body.pop()

            self.screen.blit(self.bg, (0,0))
            self.screen.blit(self.apple, food)
            snake.draw(self.screen)

            self.text(f"Score: {score}", 10, 10)
            self.text(f"Highest: {self.highest}", 620, 10, (255,220,0))

            pygame.display.flip()

    def run(self):
        while True:
            self.menu()
            self.game_over(self.play())

Game().run()