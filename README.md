# Processing Engine for Adaptive Content Extraction (PEACE)

**PEACE** is a Python-based automated video clipping tool designed to streamline the process of extracting highlights from videos. Whether you're a gamer looking to create montages, a content creator producing highlights, or simply someone who wants to save memorable moments, **PEACE** provides an efficient, easy-to-use solution.

---

## Features

- **Automatic Frame Extraction:** Extracts frames from video at specific timestamps.
- **Customizable Settings:** Allows you to set parameters for precision.
- **Fast and Lightweight:** Optimized for performance to minimize CPU and GPU usage.
- **Supports Multiple Formats:** Compatible with a variety of video formats.

---

## Installation & Execution

1. **Clone the repository:**

   ```bash
   git clone https://github.com/NakshatraSirohi/PEACE.git
   cd PEACE
   ```

2. **Install the dependencies:**

   ```bash
   pip install requirements.txt
   ```

3. **Run the script:**
   ```bash
   cd Script
   python3 main.py
   ```

---

# Script Documentation

# Overview

This script automates the process of detecting kills in a gaming video, grouping timestamps, and extracting clips around those timestamps. It uses OpenCV for image processing, FFmpeg for video manipulation, and Python for data handling.

## Modules Used

1. **os**:
   - **Purpose**: Used to handle file and directory operations.
   - **Functions**: File path manipulation `os.path()`, directory creation `os.makedirs()`.
2. **cv2 (OpenCV)**:

   - **Purpose**: Used for image processing and template matching in frames extracted from video.
   - **Functions**: Image reading, manipulation, and finding specific patterns or objects within images.

3. **ffmpeg-python**:

   - **Purpose**: A wrapper around the FFmpeg command-line tool for video processing tasks.
   - **Functions**: Frame extraction, video clipping, conversion, and processing using the FFmpeg library.

4. **ast**:

   - **Purpose**: Safely parses string representations of Python objects into actual Python objects.
   - **Functions**: `ast.literal_eval()` to convert string representations of Python lists back into actual Python objects.

5. **datetime**:

   - **Purpose**: Used to work with dates and times, particularly to generate current timestamp-based directory names or for time-based operations.
   - **Functions**: Date and time formatting, and getting current date and time using `datetime.now()`.

6. **time**:
   - **Purpose**: Used for time-related tasks such as delays and performance measurements.
   - **Functions**: `time.sleep()` for pausing execution.

---

## Folder Structure

```
PEACE/
│
├── Script/                            # Core functionality scripts
│   ├── KillFeed/                      # Directory with kill feed template images
│   |    └── kill_feed_template1.png   # Template file
|   │    └── ...                       # More templates
|   |
│   ├── main.py                        # Main entry point for the script
│   ├── createDir.py                   # Directory creation script
│   ├── screenshotting.py              # Frame extraction and processing script
│   ├── scanning.py                    # Kill detection via template matching
│   ├── timeGrouping.py                # Timestamp grouping functionality
│   └── clipping.py                    # Video clipping based on grouped timestamps
│
├── TestSample/                        # Sample data for testing and examples
|   ├── BaseDirectory/                 # Base output directory for results
|   |   ├── screenshots/               # Extracted frames from the video
|   |   ├── clips/                     # Video clips created from the grouped timestamps
|   |   └── grouping.txt               # File listing grouped timestamps
|   |
|   ├── KillFeed/                      # Folder with kill feed templates
|   └── testVideo.mp4                  # Example test video
|
└── requirements.txt                   # Python dependencies

Base_Directory/                        # Output directory (named after input video)
├── screenshots/                       # Folder containing extracted and cropped frames
│   └── frame_00001.png                # Example screenshot
│   └── frame_00002.png                # Example screenshot
│   └── ...                            # More frames
|
├── clips/                             # Folder containing extracted video clips
|   └── gameplay_clip1.mp4             # Example clip
|   └── gameplay_clip2.mp4             # Example clip
|   └── ...                            # More clips
|
└── grouping.txt                       # File listing grouped kill timestamps

```

---

## Function Descriptions

### 1. `createDir()`

**Purpose**:  
Creates a new directory for storing extracted frames, grouped timestamps, and video clips, named based on the current timestamp to ensure unique folder names.

**Input**:

- No direct inputs.

**Output**:

- A string representing the path to the newly created directory.

---

### 2. `screenshotting(original_video_location, outputDir)`

**Purpose**:  
Extracts frames from the input video at specified intervals and crops the regions containing the kill feed (using template matching). These frames are saved for further analysis.

**Input**:

- `original_video_location` (str): Path to the input video.
- `outputDir` (str): Directory where the frames will be saved.

**Output**:

- A series of cropped screenshots stored in the `screenshots/` subdirectory.

**Details**:

- The script extracts frames at a user-specified rate (e.g., once per second).
- The frames are saved as PNG images in a folder named `screenshots` within the output directory.

---

### 3. `scanning(outputDir, start_time, fps=1)`

**Purpose**:  
Scans the extracted screenshots using template matching techniques to detect kill feed patterns in each frame. The timestamp of each detected kill is saved for further processing.

**Input**:

- `outputDir` (str): Directory containing the extracted screenshots.
- `start_time` (int): The starting timestamp for the video (used to calculate absolute timestamps for kills).
- `fps` (int, optional): The number of frames per second used during screenshot extraction. Default is 1.

**Output**:

- A list of timestamps (in seconds) representing kill events detected in the video.

**Details**:

- The function uses predefined template images from the `KillFeed/` directory to match and locate kill notifications in the frames.
- The timestamps of matched templates are recorded and returned.

---

### 4. `timeGrouping(outputDir, input_time)`

**Purpose**:  
Groups detected kill timestamps into intervals if the timestamps are within a user-defined threshold (e.g., 20 seconds). This function is useful for creating highlight clips where consecutive kills occur within short intervals.

**Input**:

- `outputDir` (str): Directory to store the results of grouped timestamps.
- `input_time` (list): List of individual kill timestamps to be grouped.

**Output**:

- A file named `grouping.txt` containing the grouped timestamps, where each group corresponds to a series of kills within a time interval.

**Details**:

- If two kills are detected within 20 seconds of each other, they are grouped together into a single highlight interval.
- This helps in generating video clips around a sequence of kills.

---

### 5. `clipping(original_video_location, outputDir)`

**Purpose**:  
Clips the original video based on the grouped kill timestamps. Each clip is generated around a specific group of kills, with a defined buffer time before and after the kills to ensure smooth transitions.

**Input**:

- `original_video_location` (str): Path to the original video file.
- `outputDir` (str): Directory containing the `grouping.txt` file with grouped timestamps.

**Output**:

- A series of video clips saved in a `clips/` subdirectory within the output directory.

**Details**:

- For each group of kill timestamps, the script extracts a video clip that includes a small buffer before the first kill and after the last kill, to ensure the clip contains enough context.
- The clips are saved as `.mp4` files in the `clips/` subfolder.

---

## How to Use

1. **Prepare Kill Feed Templates**:

   - Place kill feed template images in a folder named `KillFeed` in the same directory as the script.
   - Ensure templates are in `.png` format.

2. **Run the Script**:

   - Execute the script and provide inputs when prompted:
     - Path to the input video.
     - Path to output directory.

3. **Outputs**:

   - **Screenshots**: Frames extracted from the video at specified intervals, stored in `screenshots/`.
   - **Grouping File**: `grouping.txt` containing the grouped kill timestamps.
   - **Clips**: Video clips based on the grouped timestamps, saved in `clips/`.
   - All of the above will be created in the base (output) directory.

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

- **Change Detection Threshold**: Modify the `max_val >= 0.75` condition in `scanning.py` script to adjust sensitivity.
- **Change Time Buffer for Clipping**: Modify the `start_time - 5` and `end_time + 5` logic in `clipping.py` script.

---

## Dependencies

The following Python modules are required to run the tool:

- Python 3.x
- OpenCV (`cv2`)
- FFmpeg (video processing)
- Required Python libraries: `os`, `time`, `ast`, `datetime`, `typing`

---

## Notes

- Ensure FFmpeg is installed and accessible via the system PATH.
- The `KillFeed` folder must be in the same directory as the script for proper functioning.
- I'm actively working to enhance this script and add more features for better usability and performance.

## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

## Contribution

We welcome contributions! If you have suggestions for improvements or new features, feel free to fork the repository and submit a pull request.
