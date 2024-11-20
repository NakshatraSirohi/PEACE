import createDir
import screenshotting
import scanning
import timeGrouping
import clipping

def main():
    # Get video location and output directory
    original_video_location = input("Enter video location: ")
    outputDir = createDir.createDir()

    # Get tuple from screenshotting
    start_time, fps_str = screenshotting.screenshotting(original_video_location, outputDir)

    # Process scanning result
    scanning_result = scanning.scanning(outputDir, start_time, fps_str)

    # Group times
    timeGrouping.timeGrouping(outputDir, scanning_result)

    # Process clipping
    clipping.clipping(outputDir, original_video_location)

if __name__ == "__main__":
    main()
