import pyautogui
import time
import os
from typing import Optional, Tuple


def locate_image(target_path: str, search_path: str, confidence_level: float) -> Optional[Tuple[int, int, int, int]]:
    """
    Locate the position of a target image within another image using image matching.

    Args:
        target_path (str): Path to the target image file (the smaller image to locate).
        search_path (str): Path to the search image file (the larger image where the target is searched).
        confidence_level (float): Confidence level for image matching, between 0 and 1. A higher value indicates a stricter match.

    Returns:
        Optional[Tuple[int, int, int, int]]:
            If the target image is found, returns a tuple containing:
                - left (int): The x-coordinate of the top-left corner of the found image.
                - top (int): The y-coordinate of the top-left corner of the found image.
                - width (int): The width of the found image.
                - height (int): The height of the found image.
            If the target image is not found, returns None.

    Raises:
        FileNotFoundError: If either of the provided image files cannot be found.
        Exception: For any other unforeseen error during the image matching process.
    """
    try:
        # Locate the target image within the search image
        result = pyautogui.locate(target_path, search_path, confidence=confidence_level)
        return result
    except FileNotFoundError:
        print(f"Error: File not found. Please check paths: {target_path}, {search_path}.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def main() -> None:
    """
    Main function to locate a target image within a search image.

    The target and search images are hardcoded in the script, and the script continuously
    searches for the target image in the search image until it is found. Once the target is
    located, the coordinates and dimensions of the target image are printed.

    Returns:
        None
    """
    print("Welcome to the Image Locator Tool!")

    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Hardcoded filenames for the target and search images
    target_filename = 'ss2.jpg'     # Cropped image to locate
    search_filename = 'ss1.jpg'     # Full image to search within

    # Construct full paths to the images
    target_path = os.path.join(current_directory, target_filename)
    search_path = os.path.join(current_directory, search_filename)

    # Set confidence level for image matching
    confidence_level = 0.85

    # Validate if the specified image files exist
    if not os.path.isfile(target_path) or not os.path.isfile(search_path):
        print("Error: One or both of the specified files do not exist in the current directory. Please check the filenames.")
        return

    print("Searching for the target image...")

    # Continuously search for the target image until it is found
    while True:
        result: Optional[Tuple[int, int, int, int]] = locate_image(target_path, search_path, confidence_level)
        if result:
            # Print the crop parameters (coordinates and dimensions)
            print(f"crop_x = {result[0]}\ncrop_y = {result[1]}\ncrop_width = {result[2]}\ncrop_height = {result[3]}")
            break  # Exit the loop when the target is found
        time.sleep(0.5)  # Delay to avoid excessive CPU usage during continuous searching


if __name__ == "__main__":
    main()
