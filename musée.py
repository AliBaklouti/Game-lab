import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FONT = pygame.font.Font(None, 36)
CUP_COLOR = (0, 255, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Drinking Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Game variables
player1_key = pygame.K_l
player2_key = pygame.K_s
score = 0
cups_filled = 0
cup_height = HEIGHT  # Initial height of the cup (full)
start_time = 0
time_limit = 80  # in seconds
player1_pressed = False
player2_pressed = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == player1_key:
                player1_pressed = time.time()
            elif event.key == player2_key:
                player2_pressed = time.time()

    # Check if both players pressed their keys within 0.5 seconds
    if (
        player1_pressed
        and player2_pressed
        and abs(player1_pressed - player2_pressed) <= 0.5
    ):
        # Update the cup height and reset player key presses
        cup_height -= HEIGHT // 10
        player1_pressed = player2_pressed = False

        # Check if the cup is empty
        if cup_height <= 0:
            # Increment score, reset cup height, and start a new round
            score += 1
            cups_filled += 1
            cup_height = HEIGHT
            start_time = time.time()

    # Check for game over condition (time limit reached)
    if start_time == 0:
        start_time = time.time()
    elif time.time() - start_time >= time_limit:
        running = False

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the cup
    pygame.draw.rect(
        screen, CUP_COLOR, (WIDTH // 2 - 50, HEIGHT - cup_height, 100, cup_height)
    )

    # Draw the score
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw the time remaining
    time_remaining = max(time_limit - (time.time() - start_time), 0)
    time_text = FONT.render(f"Time: {time_remaining:.1f}", True, (255, 255, 255))
    screen.blit(time_text, (WIDTH - 150, 10))

    # Update the display
    pygame.display.update()
    clock.tick(30)  # Control the frame rate (30 FPS)

# Display the final score and cups filled
while True:
    screen.fill(BACKGROUND_COLOR)
    final_score_text = FONT.render(f"Final Score: {score}", True, (255, 255, 255))
    cups_filled_text = FONT.render(f"Cups Filled: {cups_filled}", True, (255, 255, 255))
    screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
    screen.blit(cups_filled_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))
    pygame.display.update()
    pygame.time.wait(2000)  # Wait for 2 seconds before quitting

    # Handle game restart or exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Restart the game
                score = 0
                cups_filled = 0
                cup_height = HEIGHT
                start_time = 0
                player1_pressed = player2_pressed = False
            elif event.key == pygame.K_q:  # Quit the game
                pygame.quit()
                exit()
