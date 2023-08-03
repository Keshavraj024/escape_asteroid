import pygame
import time
import random
from typing import List

pygame.font.init()

WIDTH, HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BG_IMAGE_PATH = "screenshots/background.jpg"
BG = pygame.transform.scale(pygame.image.load(BG_IMAGE_PATH), (WIDTH, HEIGHT))
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 20
PLAYER_VEL = 5
STAR_WIDTH, STAR_HEIGHT = 20, 10
STAR_VEL = 5
FONT = pygame.font.SysFont("comicsans", 30)


def draw(player: pygame.Rect, elapsed_time: float, stars: List[pygame.Rect]) -> None:
    """Draw the game objects and update the display."""
    WINDOW.blit(BG, (0, 0))
    time_string = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WINDOW.blit(time_string, (10, 10))
    pygame.draw.rect(WINDOW, "red", player)
    for star in stars:
        pygame.draw.rect(WINDOW, "white", star)
    pygame.display.update()


def handle_player_movement(player: pygame.Rect, keys) -> None:
    """Handle player movement based on user input."""
    if keys[pygame.K_LEFT]:
        player.x = max(player.x - PLAYER_VEL, 0)
    if keys[pygame.K_RIGHT]:
        player.x = min(player.x + PLAYER_VEL, WIDTH - PLAYER_WIDTH)


def create_stars(
    stars: List[pygame.Rect],
    star_count: pygame.time.Clock(),
    star_time_increment: int,
    clock: pygame.time.Clock(),
) -> tuple:
    """Create stars at regular intervals"""
    star_count += clock.tick(10)
    if star_count > star_time_increment:
        num_stars_per_iteration = 3
        for _ in range(num_stars_per_iteration):
            star_pos = random.randint(0, WIDTH - STAR_WIDTH)
            star = pygame.Rect(star_pos, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
            stars.append(star)
        star_count = 0
        star_time_increment = max(400, star_time_increment - 50)
    return stars, star_count


def check_collision(stars: List[pygame.Rect], player: pygame.Rect) -> bool:
    """Check for collisions between stars and player."""
    for star in stars[:]:
        star.y += STAR_VEL
        if star.y > HEIGHT:
            stars.remove(star)
        elif star.y + STAR_HEIGHT >= player.y and star.colliderect(player):
            stars.remove(star)
            return True
    return False


def game_loop(
    level: str, total_time: int, num_levels: dict, clock: pygame.time.Clock()
) -> tuple:
    """Run the main game loop for a specific level and total_time."""
    star_time_increment = 2000
    stars = []
    start_time = time.time() + total_time
    player = pygame.Rect(100, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    hit = False
    star_count = 0

    while not hit:
        elapsed_time = start_time - time.time()
        stars, star_count = create_stars(stars, star_count, star_time_increment, clock)

        if elapsed_time < 0:
            if level == list(num_levels.keys())[-1]:
                success_msg = FONT.render(
                    f"Successfully completed all levels", 1, "white"
                )
                WINDOW.blit(
                    success_msg,
                    (
                        WIDTH // 2 - success_msg.get_width() // 2,
                        HEIGHT - success_msg.get_width() // 2,
                    ),
                )
                pygame.display.update()
                pygame.time.delay(2000)
                return False, False
            else:
                level_completion_msg = FONT.render(
                    f"Accomplished {level}. Moving on to Next Level", 1, "white"
                )
                WINDOW.blit(
                    level_completion_msg,
                    (
                        WIDTH // 2 - level_completion_msg.get_width() // 2,
                        HEIGHT - level_completion_msg.get_width() // 2,
                    ),
                )
                pygame.display.update()
                pygame.time.delay(2000)
                return False, True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, False

        handle_player_movement(player, keys=pygame.key.get_pressed())

        hit = check_collision(stars, player)

        if hit:
            lost_msg = FONT.render(
                f"YOU LOST THE GAME. Asteroid Survival Time: {round(elapsed_time)}s",
                1,
                "white",
            )
            WINDOW.blit(
                lost_msg,
                (
                    WIDTH // 2 - lost_msg.get_width() // 2,
                    HEIGHT - lost_msg.get_width() // 2,
                ),
            )
            pygame.display.update()
            pygame.time.delay(4000)
            return False, False

        draw(player, elapsed_time, stars)

    return True, False


def main() -> None:
    """Main function to run the game."""
    num_levels = {"Level 1": 30, "Level 2": 20}
    next_level = True
    for level, total_time in num_levels.items():
        if next_level:
            run = True
            pygame.init()
            pygame.display.set_caption(f"Escape the asteroids {level}")
            clock = pygame.time.Clock()
            while run:
                run, next_level = game_loop(level, total_time, num_levels, clock)
    pygame.quit()


if __name__ == "__main__":
    main()
