import os
from datetime import datetime
from typing import Optional

def createDir() -> Optional[str]:
    """
    Creates a uniquely named directory based on the current timestamp.
    Users can choose between using the current working directory or a custom directory.
    Ensures uniqueness by appending a counter if a folder with the same name already exists.

    Returns:
        str: The path of the created directory.
    """

    # Generate a timestamp in 'YYYY-MM-DD_HH-MM-SS' format for folder naming.
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Prompt the user to select a base directory.
    while True:
        try:
            choice = int(input("Set Output: (1)-Custom Directory OR (2)-Current Working Directory, Enter choice (1/2): "))
            if choice not in [1, 2]:
                raise ValueError("Invalid choice. Please enter 1 or 2.")
            break
        except ValueError as e:
            print(e)

    # Determine the base directory based on user input.
    if choice == 1:
        # Get the custom directory path from the user.
        base_directory = input("Enter custom output directory path: ").strip()

        # Check if the custom directory exists and is writable.
        if not os.path.exists(base_directory):
            print(f"Error: The directory '{base_directory}' does not exist.")
            return
        if not os.access(base_directory, os.W_OK):
            print(f"Error: The directory '{base_directory}' is not writable.")
            return
    else:
        # Default to the current working directory.
        print("Using current working directory for output.")
        base_directory = os.getcwd()

    # Create the folder path with the timestamp.
    folder = os.path.join(base_directory, timestamp)

    # Ensure the folder name is unique by appending a counter if necessary.
    counter = 1
    while os.path.exists(folder):
        folder = os.path.join(base_directory, f"{timestamp} ({counter})")
        counter += 1

    # Create the directory with the final unique name.
    try:
        os.makedirs(folder)
        print(f"Successfully Created: {folder}")
        return folder
    except OSError as e:
        print(f"Error: Could not create directory. {e}")
        return None
