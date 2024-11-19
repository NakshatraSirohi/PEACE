# Processing Engine for Adaptive Content Extraction (PEACE)

**PEACE** is a Python-based automated video clipping tool designed to streamline the process of extracting highlights from videos. Whether you're a gamer looking to create montages, a content creator producing highlights, or simply someone who wants to save memorable moments, **PEACE** provides an efficient, easy-to-use solution.

---

## Features

- **Automatic Frame Extraction:** Extracts frames from video at specific timestamps.
- **Customizable Settings:** Allows you to set parameters for precision.
- **Fast and Lightweight:** Optimized for performance to minimize CPU and GPU usage.
- **Supports Multiple Formats:** Compatible with a variety of video formats.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NakshatraSirohi/AutoClipping.git
   cd AutoClipping
   ```

---

# Script Documentation: PEACE

# Overview

This script automates the process of detecting kills in a gaming video, grouping timestamps, and extracting clips around those timestamps. It uses OpenCV for image processing, FFmpeg for video manipulation, and Python for data handling.

## Modules Used

1. **os**: Handles file and directory operations.
2. **cv2**: Used for image processing and template matching.
3. **ffmpeg**: Executes video processing tasks like frame extraction and clipping.
4. **ast**: Parses string representations of Python objects.
5. **time**: Adds delays for certain operations to ensure proper execution.

---

## Function Descriptions

### 1. `createDir(input_video_path)`

- **Purpose**: Creates a unique directory based on the input video file name for storing output files.
- **Inputs**:
  - `input_video_path` (str): Full path to the input video.
- **Outputs**:
  - Returns the path of the newly created directory.
- **Logic**: If a directory with the same name already exists, appends a numerical suffix to create a unique name.

### 2. `screenshotting(input_path, outputDir, start_time, end_time)`

- **Purpose**: Extracts screenshots from the video at a defined interval, crops the kill feed area, and saves the frames.
- **Inputs**:
  - `input_path` (str): Full path to the input video.
  - `outputDir` (str): Directory where screenshots will be saved.
  - `start_time` (int): Start time for extracting screenshots (in seconds).
  - `end_time` (int): End time for extracting screenshots (in seconds).
- **Outputs**:
  - Saves cropped screenshots in a subfolder named `screenshots`.
- **Details**:
  - Captures 2 frames every 3 seconds using FFmpeg (modifications are possible).
  - Crops a region of interest (ROI) to focus on the kill feed area.

### 3. `scanning(outputDir, start_time)`

- **Purpose**: Identifies timestamps of kills in the extracted screenshots using template matching.
- **Inputs**:
  - `outputDir` (str): Directory containing the screenshots.
  - `start_time` (int): Starting time of the video to calculate absolute kill times.
- **Outputs**:
  - Returns a list of timestamps where kills were detected.
- **Details**:
  - Loads kill feed templates from a predefined folder (`KillFeed`).
  - Uses OpenCV’s template matching to compare each screenshot with the templates.
  - Records timestamps of matches with confidence ≥ 0.75.

### 4. `timeGrouping(outputDir, input_time)`

- **Purpose**: Groups kill timestamps into intervals if they occur within 20 seconds of each other.
- **Inputs**:
  - `outputDir` (str): Directory for saving grouped intervals.
  - `input_time` (list): List of kill timestamps.
- **Outputs**:
  - Saves grouped intervals to a file named `grouping.txt`.
- **Details**:
  - Iterates through the timestamps and groups them based on a 20-second threshold.

### 5. `clipping(outputDir, input_video_path)`

- **Purpose**: Extracts video clips around the grouped kill timestamps.
- **Inputs**:
  - `outputDir` (str): Directory containing grouping results.
  - `input_video_path` (str): Full path to the input video.
- **Outputs**:
  - Saves clips in a subfolder named `clips`.
- **Details**:
  - Reads grouped intervals from `grouping.txt`.
  - Clips 5 seconds before and after each group and saves them as MP4 files.

---

## How to Use

1. **Prepare Kill Feed Templates**:

   - Place kill feed template images in a folder named `KillFeed` in the same directory as the script.
   - Ensure templates are in `.png` format.

2. **Run the Script**:

   - Execute the script and provide inputs when prompted:
     - Path to the input video.
     - Start and end times (in seconds) for screenshotting.
   - The script will create a directory based on the video name and process the video.

3. **Outputs**:
   - `screenshots`: Folder containing extracted and cropped frames.
   - `grouping.txt`: File listing grouped kill timestamps.
   - `clips`: Folder containing video clips around kill events.

---

## Error Handling

- The script skips screenshots that fail to load and logs errors with filenames.
- If FFmpeg operations fail, the script suppresses errors to prevent termination.

---

## Customization

- **Change Detection Threshold**: Modify the `max_val >= 0.75` condition in `scanning` to adjust sensitivity.
- **Adjust Frame Extraction Rate**: Update the `fps` variable in `screenshotting`.
- **Change Time Buffer for Clipping**: Modify the `start_time - 5` and `end_time + 5` logic in `clipping`.

---

## Example Workflow

1. Input video: `gameplay.mp4`.
2. Kill feed templates placed in `KillFeed` folder.
3. Start time: 60 seconds, End time: 300 seconds.
4. Output structure:
   - `gameplay/screenshots`: Contains cropped frames.
   - `gameplay/grouping.txt`: Lists kill groups.
   - `gameplay/clips`: Contains MP4 files for each group.
   - Example:- `Group-1: [65, 70, 85]` Creates a clip from `65-5=60sec` to `85+5=90sec` from the original video.

---

## Dependencies

- Python 3.x
- OpenCV (`cv2`)
- FFmpeg library
- Required Python modules (`os`, `time`, `ast`)

---

## Notes

- Ensure FFmpeg is installed and accessible via the system PATH.
- The script assumes the input video is in a supported format (e.g., MP4).
