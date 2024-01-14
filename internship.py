import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (200, 200, 200)
CARPET_COLOR = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BOX_WIDTH, BOX_HEIGHT = 50, 50
CARPET_HEIGHT = 100
SPEED_INCREASE_INTERVAL = 5  # Increase speed every 5 seconds
MAX_SPEED = 10
TIMER_DURATION = 30  # in seconds

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Box Game")

# Fonts
font = pygame.font.Font(None, 36)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Game variables
boxes = []  # List to store boxes (color, rect)
player_score = 0
speed = 2
speed_increase_timer = 0
start_time = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and boxes and boxes[0][0] == GREEN:
                player_score += 1
                boxes.pop(0)
            elif event.key == pygame.K_DOWN and boxes and boxes[0][0] == RED:
                player_score += 1
                boxes.pop(0)

    # Update game variables
    current_time = pygame.time.get_ticks() / 1000.0  # Convert milliseconds to seconds

    if start_time == 0:
        start_time = current_time

    elapsed_time = current_time - start_time

    if elapsed_time < TIMER_DURATION:
        if elapsed_time >= speed_increase_timer:
            speed_increase_timer += SPEED_INCREASE_INTERVAL
            speed = min(speed + 1, MAX_SPEED)

        # Move boxes
        for box in boxes:
            box[1].move_ip(-speed, 0)

        # Remove off-screen boxes
        boxes = [box for box in boxes if box[1].right > 0]

        # Generate new boxes
        if random.random() < 0.01:  # Probability of generating a new box
            color = random.choice([RED, GREEN])
            new_box = pygame.Rect(
                WIDTH, HEIGHT - CARPET_HEIGHT - BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT
            )
            boxes.append((color, new_box))

    else:
        running = False  # End the game when the time is up

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw carpet
    pygame.draw.rect(
        screen, CARPET_COLOR, (0, HEIGHT - CARPET_HEIGHT, WIDTH, CARPET_HEIGHT)
    )

    # Draw boxes
    for color, box_rect in boxes:
        pygame.draw.rect(screen, color, box_rect)

    # Draw score
    score_text = font.render(f"Score: {player_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Draw timer
    timer_text = font.render(
        f"Time: {max(TIMER_DURATION - elapsed_time, 0):.1f}", True, (0, 0, 0)
    )
    screen.blit(timer_text, (WIDTH - 150, 10))

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(30)  # Adjust as needed

# Display final score
final_score_text = font.render(f"Final Score: {player_score}", True, (0, 0, 0))
screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
pygame.display.update()

# Wait for 2 seconds before quitting
pygame.time.wait(2000)

# Quit Pygame
pygame.quit()
sys.exit()
