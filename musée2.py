import pygame
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FONT = pygame.font.Font(None, 36)
CUP_IMAGES = ["cup1.png", "cup2.png", "cup3.png", "cup4.png", "cup5.png", "cup6.png"]
CUP_COLOR = (0, 255, 0)
CUP_HEIGHT_LEVELS = [HEIGHT // 6 * i for i in range(7)]

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
cup_level = 5  # The initial cup level (full)
start_time = 0
time_limit = 80  # in seconds
player1_pressed = False
player2_pressed = False
initial_start_time = 0

# Load cup images
cup_images = [pygame.image.load(image) for image in CUP_IMAGES]


# Function to draw the cup image
def draw_cup():
    cup_image = cup_images[cup_level]
    screen.blit(cup_image, (200, 150))


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
        and abs(player1_pressed - player2_pressed) <= 0.05
    ):
        # Update the cup level and reset player key presses
        cup_level -= 1
        player1_pressed = player2_pressed = False

        # Check if the cup is empty
        if cup_level < 0:
            # Increment score, reset cup level, and continue with the current round
            score += 1
            cups_filled += 1
            cup_level = 5

    # Check for game over condition (time limit reached)
    if start_time == 0:
        start_time = time.time()
        initial_start_time = start_time
    elif time.time() - initial_start_time >= time_limit:
        running = False

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the cup image
    draw_cup()

    # Draw the score
    score_text = FONT.render(f"Times vomitted: {score}", True, (255, 255, 255))
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
                cup_level = 5
                start_time = 0
                player1_pressed = player2_pressed = False
                initial_start_time = 0
            elif event.key == pygame.K_q:  # Quit the game
                pygame.quit()
                exit()
