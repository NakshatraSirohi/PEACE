import os
import cv2
from fractions import Fraction
from typing import List, Optional, Any

def scanning(outputDir: str, start_time: int, fps: str = "1") -> Optional[List[int]]:
    """
    Scans the screenshots directory to detect 'kill feed' images and matches them
    with the screenshots. If a match is found, it calculates the adjusted kill time.

    Args:
        outputDir (str): The directory where the screenshots are located.
        start_time (int): The start time to offset the kill event times.
        fps (str): The FPS to adjust the kill timing according to the original video.

    Returns:
        list: A list of adjusted kill times based on the screenshots and detected kills.
    """

    try:
        # Handle fractional or integer FPS values
        if '/' in fps:
            ss_speed = float(Fraction(fps[::-1]))
        else:
            ss_speed = float(Fraction(fps))
    except ValueError:
        print("Invalid FPS format. Please enter a valid FPS (e.g., '30' or '2/3').")
        ss_speed = 1.0  # Fallback default value

    # If no start time is provided, default it to 0
    start_time = start_time or 0

    # Define the folder for storing screenshots and kill feed images
    screenshots_folder = "screenshots"
    screenshots_folder_path = os.path.join(outputDir, screenshots_folder)

    # Check if the screenshots folder exists
    if not os.path.exists(screenshots_folder_path):
        print(f"Error: Screenshots folder '{screenshots_folder_path}' not found.")
        return None

    # Initialize list to store the final calculated kill times
    output_time = []

    # Load kill feed images for pattern matching
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_script_directory)
    killFeed_directory = os.path.join(parent_directory, 'KillFeed')

    kill_feed_images = load_kill_feed_images(killFeed_directory)

    # If no kill feed images are found, return early
    if not kill_feed_images:
        print("Error: No kill feed images found.")
        return None

    # Process each screenshot in the folder
    for filename in os.listdir(screenshots_folder_path):
        full_image_path = os.path.join(screenshots_folder_path, filename)
        full_image = cv2.imread(full_image_path)

        # Ensure the image was loaded successfully
        if full_image is None:
            print(f"Warning: Could not open {filename}, skipping this image.")
            continue

        # Check for a match with kill feed images
        kill_time = match_kill_feed(full_image, kill_feed_images, filename)

        # If a match is found, calculate the adjusted kill time
        if kill_time is not None:
            adjusted_kill_time = start_time + int(float(kill_time) * ss_speed)
            output_time.append(adjusted_kill_time)
            print(f"Kill found at {filename}, adjusted time: {adjusted_kill_time} seconds.")

    return output_time


def load_kill_feed_images(kill_feed_dir: str) -> Optional[List[Any]]:
    """
    Loads all PNG images from the specified directory for kill feed pattern matching.

    Args:
        kill_feed_dir (str): Directory containing the kill feed images.

    Returns:
        list: A list of loaded images.
    """

    kill_feed_images: List[Any] = []

    # Ensure the KillFeed directory exists
    if not os.path.exists(kill_feed_dir):
        print(f"Error: KillFeed directory '{kill_feed_dir}' not found.")
        return None

    # Load all PNG images from the KillFeed directory
    for img_name in os.listdir(kill_feed_dir):
        if img_name.lower().endswith('.png'):
            img_path = os.path.join(kill_feed_dir, img_name)
            img = cv2.imread(img_path)
            if img is not None:
                kill_feed_images.append(img)
            else:
                print(f"Warning: Could not read image '{img_name}', skipping.")

    return kill_feed_images


def match_kill_feed(full_image: Any, kill_feed_images: List[Any], filename: str) -> Optional[int]:
    """
    Matches the screenshot with kill feed images using template matching.

    Args:
        full_image (numpy.ndarray): The screenshot to match.
        kill_feed_images (list): List of kill feed images to match against.
        filename (str): The name of the screenshot file for logging.

    Returns:
        int or None: The kill time extracted from the filename if a match is found, else None.
    """

    for kill_img in kill_feed_images:
        # Perform template matching between the screenshot and kill feed image
        result = cv2.matchTemplate(full_image, kill_img, cv2.TM_CCOEFF_NORMED)
        max_val = cv2.minMaxLoc(result)[1]

        # If the match quality exceeds the threshold (0.75), it's considered a kill
        if max_val >= 0.75:
            print(f"Match found in {filename} with kill feed image.")
            # Safely extract the kill time from the filename
            try:
                kill_time = int(filename.split('_')[1].split('.')[0])
                return kill_time
            except (IndexError, ValueError):
                print(f"Error: Unable to extract kill time from filename '{filename}'.")
                return None

    return None
