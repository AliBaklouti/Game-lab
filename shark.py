import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FISHING_ROD_COLOR = (0, 255, 0)
SHARK_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 255)
FONT = pygame.font.Font(None, 36)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fishing Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Game variables
player_x = WIDTH // 2
score = 0
time_remaining = 600  # in seconds
sharks = []

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Move the player's fishing rod with the mouse
    player_x = pygame.mouse.get_pos()[0]

    # Create a new shark at random positions
    if random.randint(0, 100) < 2:
        shark_x = random.randint(0, WIDTH)
        shark_y = 0
        sharks.append([shark_x, shark_y])

    # Update shark positions
    for shark in sharks:
        shark[1] += 1  # Move sharks downwards
        if shark[1] > HEIGHT:
            sharks.remove(shark)  # Remove sharks that are off-screen

    # Check for collisions with the fishing rod
    for shark in sharks:
        if (
            player_x - 50 < shark[0] < player_x + 50
            and HEIGHT - 20 < shark[1] < HEIGHT + 20
        ):
            sharks.remove(shark)
            score += 1

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the fishing rod
    pygame.draw.rect(screen, FISHING_ROD_COLOR, (player_x - 50, HEIGHT - 20, 100, 20))

    shark_image = pygame.image.load(
        "Shark.png"
    )  # Replace "shark.png" with your shark image file's name
    shark_image = pygame.transform.scale(
        shark_image, (40, 40)
    )  # Adjust the size as needed

    # Draw the sharks
    for shark in sharks:
        screen.blit(shark_image, (shark[0], shark[1]))

    # Draw the score
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw the time remaining
    time_text = FONT.render(f"Time: {time_remaining:.1f}", True, (255, 255, 255))
    screen.blit(time_text, (WIDTH - 150, 10))

    # Update the display
    pygame.display.update()

    # Reduce the time remaining
    time_remaining -= 1 / 30  # 30 FPS

    # Game over condition
    if time_remaining <= 0:
        running = False

# Display the final score
screen.fill(BACKGROUND_COLOR)
final_score_text = FONT.render(f"Final Score: {score}", True, (255, 255, 255))
screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
pygame.display.update()

# Wait for a moment before quitting
pygame.time.wait(20000)

# Quit Pygame
pygame.quit()
