# Without grayscale method

import os
import cv2
import numpy as np

# Enter root folder name
main_folder = input("Enter main folder: ")

# Enter start time of ffmpeg (in seconds)
start_time = int(input("Enter start time from ffmpeg (in sec): "))

# Folder containing the screenshots
folder_path = f'{main_folder}\\screenshots'

# Output text filename
output_file = f'{main_folder}\\{main_folder}_killtime.txt'

# Load the kill-feed images into a list
kill_feed_images = []
for i in range(0,13):
    kill_feed_images.append(cv2.imread(f'KillFeed\\Capture{i}.PNG'))

# Iterate over each image in the specified folder
for filename in os.listdir(folder_path):
    full_image_path = os.path.join(folder_path, filename)

    # Try to open the screenshots
    full_image = cv2.imread(full_image_path)

    # Check if screenshot is loaded/opened
    if full_image is None:
        print(f"Error: Could not open {filename}")
        continue

    x = np.zeros_like(full_image)
    y = cv2.rectangle(x, (80, 40), (365,235), (255, 255, 255), -1)
    z = cv2.bitwise_and(full_image, y)

    # Check each kill feed image against the screenshots
    for kill_img in kill_feed_images:
        # Template matching
        result = cv2.matchTemplate(z, kill_img, cv2.TM_CCOEFF_NORMED)

        # Get the maximum match value
        max_val = cv2.minMaxLoc(result)[1]

        # Check if the match is above the confidence 75%
        if max_val >= 0.75:
            print(f"Kill found: {filename}")
            # Extracting frame number from the filename
            kill_time = filename.split('_')[1].split('.')[0]

            # Make sure the timing is correct as per fps=2/3 (1 frame = 1.5 second)
            final_kill_time = start_time + int(float(kill_time)*1.50)

            with open(output_file, "a") as file:
                file.write(f'{final_kill_time}\n')

            break  # No need to check further if a match is found
        else:
            pass
