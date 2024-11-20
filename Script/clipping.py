import os
import ffmpeg
import ast
import time

def clipping(outputDir, original_video_location):
    """
    This function creates clips from the input video based on the killshot times specified
    in a 'grouping.txt' file. Each clip is extracted with a 5-second buffer before and after
    each killshot time.
    
    Args:
        outputDir (str): The directory where the output clips will be saved.
        original_video_location (str): Path to the original video file.
    """

    # Extract the file name (without extension) from the original video location
    file_path = os.path.basename(original_video_location)
    file_name = os.path.splitext(file_path)[0]

    # Define the directory where clips will be stored
    clip_folder = "clips"
    folder_path = os.path.join(outputDir, clip_folder)

    # Create the folder if it doesn't already exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'Created: {folder_path}')
        time.sleep(2)  # Adding a small delay for folder creation
    else:
        # If the folder exists, notify the user and exit the function
        print(f'Folder already exists: {folder_path}... Please delete the folder first.')
        return

    # Set the default ffmpeg output args to disable all streams except video (which is copied)
    ffmpeg_output_args = {
        'an': None,
        'sn': None,
    }

    if input("Want to disable audio stream in output clips (Yes/No): ").strip().lower() == "no":
        # Enable audio if user chooses not to disable it
        ffmpeg_output_args.pop('an', None)

    if input("Want to disable subtitle stream in output clips (Yes/No): ").strip().lower() == "no":
        # Enable subtitles if user chooses not to disable them
        ffmpeg_output_args.pop('sn', None)

    # Ensure the grouping.txt file exists
    input_file = os.path.join(outputDir, 'grouping.txt')
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        return

    # Open the grouping.txt file where the killshot times are stored
    with open(input_file, 'r') as infile:
        count = 1  # Initialize the clip count
        
        # Iterate through each line in the grouping file (each group of killshot times)
        for line in infile:
            try:
                # Parse the string representation of the list into an actual list
                killshot_time = ast.literal_eval(line.strip())

                # Calculate the start and end times for the clip (5 seconds before and after killshot)
                start_time = killshot_time[0] - 5
                end_time = killshot_time[-1] + 5

                # Define the output clip filename
                output_clip = os.path.join(folder_path, f'{file_name}_clip{count}.mp4')
                count += 1  # Increment the clip count

                # Executes ffmpeg command to extract the clip from the original video
                ffmpeg.input(original_video_location, ss=start_time, to=end_time) \
                    .output(output_clip, codec='copy', **ffmpeg_output_args).run()
            
            except Exception as e:
                print(f"Error processing line {line}: {e}")
                continue
