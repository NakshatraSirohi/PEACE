import createDir
import screenshotting
import scanning
import timeGrouping
import clipping
from typing import List

def main():
    # Get video location and output directory
    original_video_location = input("Enter video location: ")
    outputDir: str = createDir.createDir()

    # Get tuple from screenshotting
    start_time: int
    fps: str
    start_time, fps = screenshotting.screenshotting(original_video_location, outputDir)

    # Process scanning result
    scanning_result: List[int] = scanning.scanning(outputDir, start_time, fps)

    # Group times
    timeGrouping.timeGrouping(outputDir, scanning_result)

    # Process clipping
    clipping.clipping(outputDir, original_video_location)

if __name__ == "__main__":
    main()
