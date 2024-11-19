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
   pip install requirements.txt
   python3 PEACE.py
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

## Folder Structure

```
AutoClipping/
│
├── PEACE.py                      # The main script
├── KillFeed/                     # Folder containing kill feed template images
│   └── kill_feed_template1.png   # Example kill feed template
│   └── kill_feed_template2.png   # Example kill feed template
│
├── gameplay/                     # Output directory (named after input video)
│   ├── screenshots/              # Folder containing extracted and cropped frames
│   │   └── frame_00001.png       # Example screenshot
│   │   └── frame_00002.png       # Example screenshot
│   │   └── ...                   # More frames
│   ├── grouping.txt              # File listing grouped kill timestamps
│   │   └── [65, 70, 85]          # Example group
│   ├── clips/                    # Folder containing extracted video clips
│   │   └── gameplay_clip1.mp4    # Example clip
│   │   └── gameplay_clip2.mp4    # Example clip
│   │   └── ...                   # More clips
│
└── requirements.txt              # Required dependencies
```

---

## Function Descriptions

### 1. `createDir(input_video_path)`

- **Purpose**: Creates a unique directory based on the input video file name for storing output files.
- **Inputs**:
  - `input_video_path` (str): Full path to the input video.
- **Outputs**:
  - Returns the path of the newly created directory.

### 2. `screenshotting(input_path, outputDir, start_time, end_time)`

- **Purpose**: Extracts screenshots from the video at a defined interval, crops the kill feed area, and saves the frames.
- **Inputs**:
  - `input_path` (str): Full path to the input video.
  - `outputDir` (str): Directory where screenshots will be saved.
  - `start_time` (int): Start time for extracting screenshots (in seconds).
  - `end_time` (int): End time for extracting screenshots (in seconds).
- **Outputs**:
  - Saves cropped screenshots in a subfolder named `screenshots`.

### 3. `scanning(outputDir, start_time)`

- **Purpose**: Identifies timestamps of kills in the extracted screenshots using template matching.
- **Inputs**:
  - `outputDir` (str): Directory containing the screenshots.
  - `start_time` (int): Starting time of the video to calculate absolute kill times.
- **Outputs**:
  - Returns a list of timestamps where kills were detected.
- **Details**:
  - Loads kill feed templates from a predefined folder (`KillFeed`), which must be in the same directory as the script.

### 4. `timeGrouping(outputDir, input_time)`

- **Purpose**: Groups kill timestamps into intervals if they occur within 20 seconds of each other.
- **Inputs**:
  - `outputDir` (str): Directory for saving grouped intervals.
  - `input_time` (list): List of kill timestamps.
- **Outputs**:
  - Saves grouped intervals to a file named `grouping.txt`.

### 5. `clipping(outputDir, input_video_path)`

- **Purpose**: Extracts video clips around the grouped kill timestamps.
- **Inputs**:
  - `outputDir` (str): Directory containing grouping results.
  - `input_video_path` (str): Full path to the input video.
- **Outputs**:
  - Saves clips in a subfolder named `clips`.

---

## How to Use

1. **Prepare Kill Feed Templates**:

   - Place kill feed template images in a folder named `KillFeed` in the same directory as the script.
   - Ensure templates are in `.png` format.

2. **Run the Script**:

   - Execute the script and provide inputs when prompted:
     - Path to the input video.
     - Start and end times (in seconds) for screenshotting.

3. **Outputs**:

   - `screenshots`: Folder containing extracted and cropped frames.
   - `grouping.txt`: File listing grouped kill timestamps.
   - `clips`: Folder containing video clips around kill events.
   - All of the above will be created in the same directory as the script itself.

4. **Example Workflow**:
   - Input video: `gameplay.mp4`.
   - Kill feed templates placed in `KillFeed` folder.
   - Start time: 60 seconds, End time: 300 seconds.
   - Output structure:
     - `gameplay/screenshots`: Contains cropped frames.
     - `gameplay/grouping.txt`: Lists kill groups.
     - `gameplay/clips`: Contains MP4 files for each group.
     - Example: If `Group-1` contains kill timestamps `[65, 70, 85]`:
       - A clip will be created from `65 - 5 = 60 seconds` to `85 + 5 = 90 seconds` in the original video.

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

## Dependencies

- Python 3.x
- OpenCV (`cv2`)
- FFmpeg library
- Required Python modules (`os`, `time`, `ast`)

---

## Notes

- Ensure FFmpeg is installed and accessible via the system PATH.
- The `KillFeed` folder must be in the same directory as the script for proper functioning.
- I'm actively working to enhance this script and add more features for better usability and performance.
