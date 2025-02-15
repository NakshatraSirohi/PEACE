import os
import ffmpeg
from typing import Tuple, Dict, Optional

def screenshotting(video_location: str, outputDir: str) -> Tuple[Optional[int], str]:
    """
    Generate screenshots from a video file with optional user-defined parameters.

    Args:
        video_location (str): Path to the input video file.
        outputDir (str): Directory where the screenshots will be saved.

    Returns:
        Tuple[Optional[int], str]: Tuple containing the user-defined video start time and fps.
    """

    folderName = "screenshots"
    screenshots_folder = os.path.join(outputDir, folderName)

    # Create the folder if it doesn't already exist
    if not os.path.exists(screenshots_folder):
        os.makedirs(screenshots_folder)
        print(f'Screenshots folder created: {screenshots_folder}')
    else:
        print(f'Folder already exists: {screenshots_folder}. Please delete the folder before running the script.')
        return None, ""

    # Default parameter values
    fps = '1'
    start_time = None
    end_time = None
    crop_params = None
    use_hwaccel = True

    # User prompts for custom settings
    if input("Set custom timing? (Yes/No): ").strip().lower() == "yes":
        try:
            start_time = int(input("Enter start time in seconds: ").strip())
            end_time = int(input("Enter end time in seconds: ").strip())
        except ValueError:
            print("Invalid timing input. Defaulting to full video duration.")

    if input("Set custom FPS? (default = 1) (Yes/No): ").strip().lower() == "yes":
        fps = input("Enter FPS (e.g., '2/3' or '30'): ").strip()

    if input("Crop video? (Yes/No): ").strip().lower() == "yes":
        try:
            crop_width = 364
            crop_height = 183
            crop_x = 1415
            crop_y = 74
            crop_params = (crop_width, crop_height, crop_x, crop_y)
        except ValueError:
            print("Invalid cropping input. Skipping cropping.")

    try:
        # Prepare ffmpeg input arguments
        ffmpeg_input_args: Dict[str, Optional[int | str]] = {}
        if start_time is not None:
            ffmpeg_input_args['ss'] = start_time
        if end_time is not None:
            ffmpeg_input_args['to'] = end_time
        if use_hwaccel:
            ffmpeg_input_args['hwaccel'] = 'cuda'

        # Apply filters based on user choices
        ffmpeg_input = ffmpeg.input(video_location, **ffmpeg_input_args)
        if fps:
            ffmpeg_input = ffmpeg_input.filter("fps", fps=fps)
        if crop_params:
            ffmpeg_input = ffmpeg_input.filter("crop", *crop_params)

        # Generate screenshots
        ffmpeg_input.output(os.path.join(screenshots_folder, 'frame_%05d.png'), an=None, sn=None).run()
        print("Screenshots successfully generated!")

    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode('utf8')}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return start_time, fps
