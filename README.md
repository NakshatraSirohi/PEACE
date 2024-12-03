# Processing Engine for Adaptive Content Extraction (PEACE)

**PEACE** is a Python-based automated video clipping tool designed to streamline the process of extracting highlights from videos. Whether you're a gamer looking to create montages, a content creator producing highlights, or simply someone who wants to save memorable moments, **PEACE** provides an efficient, easy-to-use solution.

---

## Features

-   **Automatic Frame Extraction:** Extracts frames from video at specific timestamps.
-   **Customizable Settings:** Allows you to set parameters for precision.
-   **Fast and Lightweight:** Optimized for performance to minimize CPU and GPU usage.
-   **Supports Multiple Formats:** Compatible with a variety of video formats.

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
├── ImageLocator/                      # Script to detect the desired cropped region
|   ├── locate_image.py                # Script to locate and provide coordinates
|   ├── full_image.png                 # Image to locate cropped_image
|   └── cropped_image.png              # Image to search in full_image
|
├── Script/                            # Core functionality scripts
│   ├── KillFeed/                      # Directory with kill feed template images
│   |    └── template.png              # Template file
│   |    └── ...                       # More templates
|   |
│   ├── main.py                        # Main entry point for the script
|   |
|   └── modules/
│       ├── createDir.py               # Directory creation script
│       ├── screenshotting.py          # Frame extraction and processing script
│       ├── scanning.py                # Kill detection via template matching
│       ├── timeGrouping.py            # Timestamp grouping functionality
│       └── clipping.py                # Video clipping based on grouped timestamps
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

-   The script skips screenshots that fail to load and logs errors with filenames.
-   If FFmpeg operations fail, the script suppresses errors to prevent termination.

---

## Customization

-   **Change Detection Threshold**: Modify the `max_val >= 0.75` condition in `scanning.py` script to adjust sensitivity.
-   **Change Time Buffer for Clipping**: Modify the `start_time - 5` and `end_time + 5` logic in `clipping.py` script.

---

## Dependencies

The following Python modules are required to run the tool:

-   Python 3.x
-   OpenCV (`cv2`)
-   FFmpeg (video processing)
-   Required Python libraries: `os`, `time`, `ast`, `datetime`, `typing`

---

## Notes

-   Ensure FFmpeg is installed and accessible via the system PATH.
-   The `KillFeed` folder must be in the same directory as the script for proper functioning.
-   I'm actively working to enhance this script and add more features for better usability and performance.

## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

## Contribution

We welcome contributions! If you have suggestions for improvements or new features, feel free to fork the repository and submit a pull request.
