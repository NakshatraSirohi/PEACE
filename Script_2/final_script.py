import os
import cv2
import ffmpeg
import ast
import time


def createDir(input_video_path):
    file_path = os.path.basename(input_video_path)
    file_name = os.path.splitext(file_path)[0]

    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, file_name)

    counter = 1
    while os.path.exists(folder_path):
        file_name = f'{file_name}_{counter}'
        folder_path = os.path.join(current_directory, file_name)
        counter += 1

    os.makedirs(folder_path)
    print(f'Created: {folder_path}')
    return folder_path


def screenshotting(input_path, outputDir, start_time, end_time):
    folderName = "screenshots"
    ss_folder = os.path.join(outputDir, folderName)

    os.makedirs(ss_folder)
    print(f'Created: {ss_folder}')
    time.sleep(2)

    fps1 = "2/3"
    crop_width = 430
    crop_height = 245
    crop_x = 1370
    crop_y = 55
    try:
        (
            ffmpeg
            .input(input_path, ss=start_time, to=end_time, hwaccel="cuda")
            .filter("fps", fps=fps1)
            .filter("crop", crop_width, crop_height, crop_x, crop_y)
            .output(os.path.join(ss_folder, 'frame_%05d.png'), an=None, sn=None)
            .run()
        )
    except:
        pass


def scanning(outputDir, start_time):
    ss_folder = "screenshots"
    folder_path = os.path.join(outputDir, ss_folder)

    output_time = []

    kill_feed_images = []
    for img in os.listdir('KillFeed'):
        if img.lower().endswith('.png'):
            tmp = cv2.imread(os.path.join('KillFeed', img))
            kill_feed_images.append(tmp)

    for filename in os.listdir(folder_path):
        full_image_path = os.path.join(folder_path, filename)
        full_image = cv2.imread(full_image_path)

        if full_image is None:
            print(f"Error: Could not open {filename}")
            continue

        for kill_img in kill_feed_images:
            result = cv2.matchTemplate(full_image, kill_img, cv2.TM_CCOEFF_NORMED)
            max_val = cv2.minMaxLoc(result)[1]

            if max_val >= 0.75:
                print(f"Kill found: {filename}")
                kill_time = filename.split('_')[1].split('.')[0]
                final_kill_time = start_time + int(float(kill_time)*1.50)
                output_time.append(final_kill_time)
                break
            else:
                pass

    return output_time


def timeGrouping(outputDir, input_time):
    output_file = f'{outputDir}\\grouping.txt'

    all_groups = []
    current_group = [input_time[0]]
    a = input_time[0]

    for i in range(1, len(input_time)):
        if input_time[i] - a <= 20:
            current_group.append(input_time[i])
        else:
            all_groups.append(current_group)
            current_group = [input_time[i]]
            a = input_time[i]

    all_groups.append(current_group)

    with open(output_file, "a") as file:
        for index, group in enumerate(all_groups):
            print(f'Group-{index}: {group}')
            file.write(f'{group}\n')


def clipping(outputDir, input_video_path):
    file_path = os.path.basename(input_video_path)
    file_name = os.path.splitext(file_path)[0]

    clip_folder = "clips"
    folder_path = os.path.join(outputDir, clip_folder)

    os.makedirs(folder_path)
    print(f'Created: {folder_path}')
    time.sleep(2)

    input_file = f'{outputDir}\\grouping.txt'
    with open(input_file, 'r') as infile:
        count = 1
        for line in infile:
            killshot_time = ast.literal_eval(line.strip())
            
            start_time = killshot_time[0] - 5
            end_time = killshot_time[-1] + 5

            output_clip = f'{folder_path}\\{file_name}_clip{count}.mp4'
            count += 1

            ffmpeg.input(input_video_path, ss=start_time, to=end_time).output(output_clip, codec='copy', an=None).run()


video_location = input("Enter video location: ")
outputDir = createDir(video_location)

start_time = int(input("Enter screenshotting start time (in sec): "))
end_time = int(input("Enter screenshotting end time (in sec): "))
screenshotting(video_location, outputDir, start_time, end_time)

scanning_result = scanning(outputDir, start_time)
timeGrouping(outputDir, scanning_result)

clipping(outputDir, video_location)