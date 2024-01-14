import cv2
import time

# Initialize the camera
camera = cv2.VideoCapture(0)  # Use the default camera (change if needed)

# Duration of the camera operation in seconds
total_duration = 10

# Interval between each photo capture in seconds
photo_interval = 2

# Folder to save the captured photos
output_folder = "captured_photos"

# Create the output folder if it doesn't exist
import os

os.makedirs(output_folder, exist_ok=True)

# Calculate the number of photos to capture
num_photos = total_duration // photo_interval

# Capture photos
for i in range(num_photos):
    # Capture a frame from the camera
    ret, frame = camera.read()

    if ret:
        # Save the frame as a .png file
        file_name = f"{output_folder}/photo_{i + 1}.png"
        cv2.imwrite(file_name, frame)
        print(f"Photo captured and saved: {file_name}")

    # Wait for the specified interval before capturing the next photo
    time.sleep(photo_interval)

# Release the camera
camera.release()
