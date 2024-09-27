# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time

# Set the video path and buffer size directly in the script
video_path = "vdo/ball-red-roboticsVision.mp4"  # Change this to your video path
buffer_size = 64

# define the lower and upper boundaries of the red ball in the HSV color space
redLower1 = (0, 120, 70)
redUpper1 = (10, 255, 255)
redLower2 = (170, 120, 70)
redUpper2 = (180, 255, 255)

# define the lower and upper boundaries for skin color in the HSV color space
skinLower = (0, 20, 70)
skinUpper = (20, 255, 255)

pts = deque(maxlen=buffer_size)

# If video path is None, grab the reference to the webcam
if not video_path:
    vs = VideoStream(src=0).start()
# Otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(video_path)

# Allow the camera or video file to warm up
time.sleep(2.0)

# Keep looping
while True:
    # Grab the current frame
    frame = vs.read()

    # Handle the frame from VideoCapture or VideoStream
    frame = frame[1] if video_path else frame

    # If we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    # Resize the frame, blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Construct masks for the color "red" and combine them
    mask1 = cv2.inRange(hsv, redLower1, redUpper1)
    mask2 = cv2.inRange(hsv, redLower2, redUpper2)
    red_mask = cv2.bitwise_or(mask1, mask2)
    red_mask = cv2.erode(red_mask, None, iterations=2)
    red_mask = cv2.dilate(red_mask, None, iterations=2)

    # Construct a mask for skin color and subtract it from the red mask
    skin_mask = cv2.inRange(hsv, skinLower, skinUpper)
    red_mask = cv2.subtract(red_mask, skin_mask)

    # Find contours in the mask and initialize the current (x, y) center of the ball
    cnts = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    centers = []

    # Only proceed if at least one contour was found
    if len(cnts) > 0:
        # Loop over the contours
        for c in cnts:
            # Find the minimum enclosing circle and centroid
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            if M["m00"] > 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # Only proceed if the radius meets a minimum size
                if radius > 10:
                    # Calculate the circularity
                    perimeter = cv2.arcLength(c, True)
                    area = cv2.contourArea(c)
                    if perimeter > 0:
                        circularity = 4 * np.pi * (area / (perimeter * perimeter))
                        # Only consider the contour if it is circular
                        if 0.7 < circularity < 1.3:
                            # Draw the circle and centroid on the frame
                            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                            cv2.circle(frame, center, 5, (0, 0, 255), -1)
                            centers.append(center)

    # Update the points queue
    for center in centers:
        pts.appendleft(center)

    # Loop over the set of tracked points
    for i in range(1, len(pts)):
        # If either of the tracked points are None, ignore them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # Otherwise, compute the thickness of the line and draw the connecting lines
        thickness = int(np.sqrt(buffer_size / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # Show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # If the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# If we are not using a video file, stop the camera video stream
if not video_path:
    vs.stop()
# Otherwise, release the camera
else:
    vs.release()

# Close all windows
cv2.destroyAllWindows()
