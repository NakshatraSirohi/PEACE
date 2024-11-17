import ffmpeg
import ast

main_folder = input("Enter main folder: ")
input_file = f'{main_folder}\\{main_folder}_grouping.txt'

with open(input_file, 'r') as infile:
    count = 1
    for line in infile:
        # Convert the string line to a Python list
        killshot_time = ast.literal_eval(line.strip())
        
        start_time = killshot_time[0] - 5
        end_time = killshot_time[-1] + 5

        # Input and output file paths
        input_vid = f'{main_folder}\\{main_folder}.mp4'
        output_clip = f'{main_folder}\\clips\\{main_folder}_clip{count}.mp4'
        count += 1

        # Extract the clip without changing quality, FPS, or bitrate
        ffmpeg.input(input_vid, ss=start_time, to=end_time).output(output_clip, codec='copy', an=None).run()

        print(f"Processed clip {count-1}: Start time {start_time}, End time {end_time}")
