import pygame
import random
import sys
import cv2
import time
import os

# Initialize Pygame
pygame.init()

# Initialize the camera
camera = cv2.VideoCapture(0)  # Use the default camera (change if needed)


# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
FLASH_COLOR = (255, 255, 255)
CAMERA_COLOR = (255, 0, 0)
FONT = pygame.font.Font(None, 36)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Photography Game (Two Players)")

# Game variables
# flash_duration = 1.0  # Fixed flash duration in seconds
# time_between_flashes = 2.0  # Random time between flashes
flash_start_time = 0
flash_visible = False
output_folder = "captured_photos"
os.makedirs(output_folder, exist_ok=True)

# Load camera icon
camera_icon = pygame.image.load("camera.png")
camera_icon = pygame.transform.scale(camera_icon, (200, 200))

# Timer variables
total_game_duration = 30  # Total game duration in seconds
game_start_time = 0

# Player variables
player1_key = pygame.K_s
player2_key = pygame.K_l
player1_pressed_time = None
player2_pressed_time = None
score_player1 = 0
score_player2 = 0

# Main game loop
running = True
i = 0
while running:
    flash_duration = random.randint(10, 20) / 10  # Fixed flash duration in seconds
    time_between_flashes = random.randint(20, 30) / 10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == player1_key and flash_visible:
                player1_pressed_time = pygame.time.get_ticks() / 1000.0
            elif event.key == player2_key and flash_visible:
                player2_pressed_time = pygame.time.get_ticks() / 1000.0

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the camera icon in the middle of the screen
    camera_rect = camera_icon.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(camera_icon, camera_rect)

    # Check if it's time to show the flash
    current_time = pygame.time.get_ticks() / 1000.0  # Convert milliseconds to seconds

    if game_start_time == 0:
        game_start_time = current_time

    remaining_time = max(total_game_duration - (current_time - game_start_time), 0)

    if remaining_time > 0:
        if (
            not flash_visible
            and current_time - flash_start_time >= time_between_flashes
        ):
            flash_visible = True
            flash_start_time = current_time
            player1_pressed_time = (
                player2_pressed_time
            ) = None  # Reset player pressed times
        elif flash_visible and current_time - flash_start_time >= flash_duration:
            flash_visible = False
            if player1_pressed_time is not None and player2_pressed_time is not None:
                # Compare the times and award a point to the fastest player
                if player1_pressed_time < player2_pressed_time:
                    score_player1 += 1
                elif player2_pressed_time < player1_pressed_time:
                    score_player2 += 1
    else:
        running = False  # End the game when the time is up

    # Draw the flash if it's visible
    if flash_visible:
        ret, frame = camera.read()
        if ret:
            file_name = f"{output_folder}/photo_{i}.png"
            cv2.imwrite(file_name, frame)
        flash = pygame.image.load(file_name)
        flash = pygame.transform.scale(flash, (400, 400))
        flash_rect = camera_icon.get_rect(center=(WIDTH // 4, HEIGHT // 4))
        screen.blit(flash, flash_rect)

    # Draw the scores on the screen
    score_player1_text = FONT.render(
        f"Player 1 Score: {score_player1}", True, (255, 255, 255)
    )
    score_player2_text = FONT.render(
        f"Player 2 Score: {score_player2}", True, (255, 255, 255)
    )
    screen.blit(score_player1_text, (10, 10))
    screen.blit(score_player2_text, (10, 50))

    # Draw the timer on the screen
    timer_text = FONT.render(f"Time: {remaining_time:.1f}", True, (255, 255, 255))
    screen.blit(timer_text, (WIDTH - 150, 10))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
