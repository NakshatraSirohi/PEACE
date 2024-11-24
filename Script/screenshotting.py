import os
import ffmpeg
from typing import Tuple, Dict, Optional

def screenshotting(original_video_location: str, outputDir: str) -> Tuple[int, str]:
    """
    Generate screenshots from a video file with optional user-defined parameters.
    
    Args:
        original_video_location (str): Path to the input video file.
        outputDir (str): Directory where the screenshots will be saved.
    
    Returns:
        tuple(start_time, str(fps)): Tuple of user-defined video start time & fps.
    """

    folderName = "screenshots"
    screenshots_folder = os.path.join(outputDir, folderName)

    # Create the folder if it doesn't already exist
    if not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)
        print(f'Screenshots Folder Created: {screenshots_folder}')
    else:
        # If the folder exists, notify the user and exit the function
        print(f'Folder already exists: {screenshots_folder}... Please delete the folder first.')
        return ()

    # Default values for parameters
    fps = '1'
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    crop_width: Optional[int] = None
    crop_height: Optional[int] = None
    crop_x: Optional[int] = None
    crop_y: Optional[int] = None
    use_hwaccel = False

    # Prompt for custom settings
    if input("Want to set custom timing? (Yes/No): ").strip().lower() == "yes":
        try:
            start_time = int(input("Enter start time in seconds: "))
            end_time = int(input("Enter end time in seconds: "))
        except ValueError:
            print("Invalid timing input. Using default timing (full video).")

    if input("Want to set custom FPS? (default fps = 1) (Yes/No): ").strip().lower() == "yes":
        fps = input("Enter FPS (e.g., '2/3' or '30'): ").strip()

    if input("Want to crop the video? (Yes/No): ").strip().lower() == "yes":
        try:
            crop_width = int(input("Enter crop width: "))
            crop_height = int(input("Enter crop height: "))
            crop_x = int(input("Enter crop X offset: "))
            crop_y = int(input("Enter crop Y offset: "))
        except ValueError:
            print("Invalid cropping input. Skipping cropping.")

    # Check if the user want to use hardware acceleration (CUDA)
    if input("Do you want to use hardware acceleration (CUDA)? (Yes/No): ").strip().lower() == "yes":
        use_hwaccel = True

    try:
        # Prepare the ffmpeg input
        ffmpeg_input_args: Dict[str, int] = {}
        if start_time is not None:
            ffmpeg_input_args['ss'] = start_time
        if end_time is not None:
            ffmpeg_input_args['to'] = end_time
        if use_hwaccel:
            ffmpeg_input_args['hwaccel'] = 'cuda'

        ffmpeg_input = ffmpeg.input(original_video_location, **ffmpeg_input_args)

        # Apply filters based on user choices
        if fps:
            ffmpeg_input = ffmpeg_input.filter("fps", fps=fps)
        if (crop_width and crop_height and crop_x and crop_y):
            ffmpeg_input = ffmpeg_input.filter("crop", crop_width, crop_height, crop_x, crop_y)

        # Run ffmpeg to output screenshots
        ffmpeg_input.output(os.path.join(screenshots_folder, 'frame_%05d.png'), an=None, sn=None).run()
        print("Screenshots successfully generated!")

    except ffmpeg.Error as e:
        print(f"An error occurred while processing the video: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return start_time, str(fps)
