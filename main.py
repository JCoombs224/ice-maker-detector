import time
import cv2
import numpy as np
import http.client, urllib
from dotenv import load_dotenv
import os

last_notification_time = 0
# Load environment variables from the .env file
load_dotenv()

def monitor_rtsp_stream(rtsp_url, roi, threshold=150, min_area=500, delay=1.0):
    # Capture the RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Cannot open RTSP stream.")
        return

    # print("Monitoring Ice Maker...")
    while True:
        # Read a frame from the stream
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame from stream.")
            break

        # Define the region of interest (ROI)
        x, y, w, h = roi
        roi_frame = frame[y:y+h, x:x+w]

        # Convert the ROI to the HSV color space
        hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

        # Define the range for the red color in HSV
        lower_red1 = np.array([0, 70, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 70, 50])
        upper_red2 = np.array([180, 255, 255])

        # Create masks for the red color
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = mask1 | mask2

        # Perform morphological operations to remove noise
        kernel = np.ones((3, 3), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

        # Find contours in the mask
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Check for red light detection
        for contour in contours:
            if cv2.contourArea(contour) > min_area:
                global last_notification_time
                current_time = time.time()
                if current_time - last_notification_time >= 300:
                    last_notification_time = current_time
                    ice_ready()

        # Display the ROI and mask for debugging purposes
        cv2.imshow('ROI', roi_frame)
        # cv2.imshow('Red Mask', red_mask)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Add a delay to slow down the frame processing
        # time.sleep(delay)

    # Release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

def ice_ready():
    # Send notification using Pushover API
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": os.getenv("PUSHOVER_API_TOKEN"),
        "user": os.getenv("PUSHOVER_USER_KEY"),
        "message": "Ice is ready!",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

    print("Ice is ready!")

if __name__ == "__main__":
    # Example RTSP URL (replace with your actual URL)
    rtsp_url = os.getenv("RTSP_URL")
    # Define the ROI (x, y, width, height)
    roi = (233, 60, 40, 47)
    delay = 5.0
    monitor_rtsp_stream(rtsp_url, roi, 150, 10, 1.0)
