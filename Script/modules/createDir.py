import os
from datetime import datetime
from typing import Optional

def createDir(base_directory: Optional[str], use_current_dir: bool) -> Optional[str]:
    """
    Creates a uniquely named directory based on the current timestamp.
    Ensures uniqueness by appending a counter if a folder with the same name already exists.

    Args:
        base_directory (str, optional): Custom directory path for folder creation.
        use_current_dir (bool, optional): If True, use the current working directory.

    Returns:
        str: The path of the created directory, or None if creation failed.
    """
    
    # Generate a timestamp for the folder name
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Determine the base directory
    if use_current_dir:
        base_directory = os.getcwd()
        print("Using current working directory for output.")
    else:
        base_directory = base_directory.strip()

        # Validate the custom directory
        if not os.path.exists(base_directory):
            print(f"Error: The directory '{base_directory}' does not exist.")
            return None
        if not os.access(base_directory, os.W_OK):
            print(f"Error: The directory '{base_directory}' is not writable.")
            return None

    # Create the folder path
    folder = os.path.join(base_directory, timestamp)

    # Ensure the folder name is unique
    counter = 1
    while os.path.exists(folder):
        folder = os.path.join(base_directory, f"{timestamp} ({counter})")
        counter += 1

    # Attempt to create the directory
    try:
        os.makedirs(folder)
        print(f"Successfully created directory: {folder}")
        return folder
    except OSError as e:
        print(f"Error creating directory: {e}")
        return None
