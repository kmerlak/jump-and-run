import pygame
import sys

pygame.init()

WIDTH = 1000
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Jump & Run")
clock = pygame.time.Clock()

SKY = (100, 180, 255)
GREEN = (70, 180, 80)
DARK_GREEN = (40, 130, 50)
BROWN = (130, 80, 40)
YELLOW = (255, 220, 40)
RED = (220, 50, 50)
BLUE = (50, 80, 220)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

player = pygame.Rect(100, 400, 40, 60)

player_x = 100
player_y = 400
player_width = 40
player_height = 60

velocity_y = 0
speed = 5
jump_strength = -14
gravity = 0.7

on_ground = False

platforms = [
    pygame.Rect(0, 520, 1000, 80),
    pygame.Rect(180, 430, 150, 25),
    pygame.Rect(400, 350, 150, 25),
    pygame.Rect(650, 430, 150, 25),
    pygame.Rect(820, 300, 120, 25),
]

coins = [
    pygame.Rect(230, 390, 20, 20),
    pygame.Rect(450, 310, 20, 20),
    pygame.Rect(700, 390, 20, 20),
    pygame.Rect(860, 260, 20, 20),
]

score = 0

enemies = [
    {
        "rect": pygame.Rect(350, 480, 40, 40),
        "speed": 2,
        "direction": 1
    },
    {
        "rect": pygame.Rect(580, 480, 40, 40),
        "speed": 3,
        "direction": -1
    }
]

goal = pygame.Rect(900, 240, 40, 60)

game_won = False
game_over = False

font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 80)


def reset_game():
    global player_x, player_y, velocity_y
    global score, game_won, game_over

    player_x = 100
    player_y = 400
    velocity_y = 0
    score = 0
    game_won = False
    game_over = False

    coins.clear()
    coins.extend([
        pygame.Rect(230, 390, 20, 20),
        pygame.Rect(450, 310, 20, 20),
        pygame.Rect(700, 390, 20, 20),
        pygame.Rect(860, 260, 20, 20),
    ])


while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_r and (game_won or game_over):
                reset_game()

    if not game_won and not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += speed

        player_x = max(0, min(WIDTH - player_width, player_x))

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and on_ground:
            velocity_y = jump_strength

        velocity_y += gravity
        player_y += velocity_y

        player.x = int(player_x)
        player.y = int(player_y)

        on_ground = False

        for platform in platforms:
            if player.colliderect(platform):
                if velocity_y > 0 and player.bottom <= platform.bottom:
                    player.bottom = platform.top
                    player_y = player.y
                    velocity_y = 0
                    on_ground = True
                elif velocity_y < 0:
                    player.top = platform.bottom
                    player_y = player.y
                    velocity_y = 0

        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                score += 10

        for enemy in enemies:
            rect = enemy["rect"]
            rect.x += enemy["speed"] * enemy["direction"]

            if rect.left <= 0 or rect.right >= WIDTH:
                enemy["direction"] *= -1

            if player.colliderect(rect):
                game_over = True

        if player.top > HEIGHT:
            game_over = True

        if player.colliderect(goal):
            game_won = True

    screen.fill(SKY)

    pygame.draw.circle(screen, WHITE, (150, 100), 35)
    pygame.draw.circle(screen, WHITE, (190, 100), 45)
    pygame.draw.circle(screen, WHITE, (230, 100), 30)

    pygame.draw.circle(screen, WHITE, (700, 120), 30)
    pygame.draw.circle(screen, WHITE, (735, 120), 40)
    pygame.draw.circle(screen, WHITE, (775, 120), 25)

    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform)
        pygame.draw.rect(
            screen,
            DARK_GREEN,
            (platform.x, platform.y, platform.width, 8)
        )

    for coin in coins:
        pygame.draw.circle(screen, YELLOW, coin.center, 10)
        pygame.draw.circle(screen, (255, 170, 0), coin.center, 10, 3)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy["rect"])

        pygame.draw.circle(
            screen,
            WHITE,
            (enemy["rect"].x + 12, enemy["rect"].y + 12),
            6
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (enemy["rect"].x + 28, enemy["rect"].y + 12),
            6
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (enemy["rect"].x + 12, enemy["rect"].y + 12),
            3
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (enemy["rect"].x + 28, enemy["rect"].y + 12),
            3
        )

    pygame.draw.rect(screen, BLACK, (goal.x, goal.y, 5, 60))

    pygame.draw.polygon(
        screen,
        GREEN,
        [
            (goal.x + 5, goal.y),
            (goal.x + 45, goal.y + 15),
            (goal.x + 5, goal.y + 30)
        ]
    )

    pygame.draw.rect(screen, BLUE, player)

    pygame.draw.circle(screen, WHITE, (player.x + 12, player.y + 15), 6)
    pygame.draw.circle(screen, WHITE, (player.x + 28, player.y + 15), 6)

    pygame.draw.circle(screen, BLACK, (player.x + 12, player.y + 15), 3)
    pygame.draw.circle(screen, BLACK, (player.x + 28, player.y + 15), 3)

    score_text = font.render(f"Coins: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))

    controls = font.render(
        "A/D or <-/-> = Move    SPACE = Jump",
        True,
        BLACK
    )

    screen.blit(controls, (20, 55))

    if game_won:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        text = big_font.render("YOU WIN!", True, YELLOW)

        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                200
            )
        )

        text2 = font.render(
            f"Coins collected: {score}    Press R to restart",
            True,
            WHITE
        )

        screen.blit(
            text2,
            (
                WIDTH // 2 - text2.get_width() // 2,
                300
            )
        )

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        text = big_font.render("GAME OVER", True, RED)

        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                200
            )
        )

        text2 = font.render(
            "Press R to restart",
            True,
            WHITE
        )

        screen.blit(
            text2,
            (
                WIDTH // 2 - text2.get_width() // 2,
                300
            )
        )

    pygame.display.flip()
