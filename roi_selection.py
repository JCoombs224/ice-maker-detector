import cv2
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def select_roi_from_rtsp(rtsp_url):
    # Capture the RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Cannot open RTSP stream.")
        return

    # Read a frame from the stream
    ret, frame = cap.read()
    if not ret:
        print("Error: Cannot read frame from stream.")
        return

    # Allow the user to select the ROI
    print("Select the region of interest (ROI) and press ENTER or SPACE to confirm.")
    roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)

    # Print the selected ROI coordinates
    print(f"Selected ROI: x={roi[0]}, y={roi[1]}, width={roi[2]}, height={roi[3]}")

    # Release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

    return roi

if __name__ == "__main__":
    # Example RTSP URL (replace with your actual URL)
    rtsp_url = os.getenv("RTSP_URL")
    selected_roi = select_roi_from_rtsp(rtsp_url)
    print(f"Selected ROI: {selected_roi}")