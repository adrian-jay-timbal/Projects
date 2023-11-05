import cv2
import imutils
import time
import keyboard
import os

# Choose the camera index (0 for the default camera, 1, 2, etc. for other cameras)
camera_index = 1  # Change this to the desired camera index

# Initialize video capture
cap = cv2.VideoCapture(camera_index)

# Create the motion detector
fgbg = cv2.createBackgroundSubtractorMOG2()

# Initialize variables
motion_detected = False
last_motion_time = None
video_writer = None
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_directory = "recorded_videos"
os.makedirs(output_directory, exist_ok=True)

video_base_filename = "motion_capture"
video_filename = None
video_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame and apply motion detection
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)

    # Check for motion
    if cv2.countNonZero(fgmask) > 2000:  # Adjust the threshold as needed
        if not motion_detected:
            print("Motion detected!")
            motion_detected = True
            last_motion_time = time.time()

            if video_writer is None:
                video_counter += 1
                video_filename = os.path.join(output_directory, f"{video_base_filename}_{video_counter}.avi")
                video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                print("Recording started!")

        if video_writer:
            video_writer.write(frame)
    else:
        if motion_detected and time.time() - last_motion_time >= 10:
            print("Motion stopped!")
            motion_detected = False
            if video_writer:
                video_writer.release()
                print(f"Recording stopped and saved to {video_filename}")
                video_writer = None

    if keyboard.is_pressed('q'):
        break

cap.release()
cv2.destroyAllWindows()
