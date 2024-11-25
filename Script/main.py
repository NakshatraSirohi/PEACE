import os
from typing import List, Optional
import Script.modules.createDir as createDir
import Script.modules.screenshotting as screenshotting
import Script.modules.scanning as scanning
import Script.modules.timeGrouping as timeGrouping
import Script.modules.clipping as clipping

def directory() -> Optional[bool]:
    base_directory = None
    use_current_dir = True
    while True:
        choice = int(input("Directory for output: (1)Custom, (2)Default: "))
        try:
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
            return None
        if not os.access(base_directory, os.W_OK):
            print(f"Error: The directory '{base_directory}' is not writable.")
            return None
        
        use_current_dir = False  # Custom directory, use_current_dir should be False.
    else:
        pass

    return base_directory, use_current_dir

def main() -> None:
    # Get video location and output directory
    video_location = input("Enter video location: ")
    
    # Validate that the video file exists
    if not os.path.exists(video_location):
        print(f"Error: The file at {video_location} does not exist.")
        return None
    
    # Create the output directory
    base_directory, use_current_dir = directory()
    outputDir: str = createDir.createDir(base_directory, use_current_dir)

    # Get tuple from screenshotting
    try:
        start_time, fps = screenshotting.screenshotting(video_location, outputDir)
    except Exception as e:
        print(f"Error during screenshot extraction: {e}")
        return None

    # Process scanning result
    scanning_result: List[int] = scanning.scanning(outputDir, start_time, fps)
    if not scanning_result:
        print("No killshots detected. Exiting...")
        return None

    # Group times
    try:
        timeGrouping.timeGrouping(outputDir, scanning_result)
    except Exception as e:
        print(f"Error during time grouping: {e}")
        return None

    # Process clipping
    try:
        clipping.clipping(video_location, outputDir)
    except Exception as e:
        print(f"Error during video clipping: {e}")
        return None

if __name__ == "__main__":
    main()
