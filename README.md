# Ice Maker Red Light Detection

This project is designed to detect when the red light on your ice maker turns on, indicating that the ice is ready. It uses a small region of interest (ROI) from a local RTSP camera stream for video input. <br>

When the ice is indicated as ready, it will send a push notification using [Pushover](https://pushover.net/). (I have it set up to send a notification to my iPhone) <br>

I made this project because I use a counter top ice maker, which does not keep the ice frozen after making it. Instead the ice in the basket will melt back into the reservoir and continue to make new ice. To not waste electricity I keep the ice it makes in my freezer, but I will forget to do this at times, which is why I made this quick project.<br>

I don't really expect anyone else to have a use for this but I thought it was a fun to make so I decided to add it to my GitHub.

## Features

- Detects when the red light on the ice maker turns on.
- Uses a local RTSP camera stream for video input.
- Allows selection of a region of interest (ROI) for more accurate detection.

## Usage
1. Ensure your RTSP camera is set up and streaming.
2. Run the ROI selection script to define the area where the red light appears.
3. Run the detection script to start monitoring the ice maker.