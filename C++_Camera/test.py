import cv2
import numpy as np

# Read the image
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video capture")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read the frame")
        break
    
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to grayscale image 
    thresh = 128
    max_value = 255
    _ , binary_img = cv2.threshold(gray_img, thresh, max_value, cv2.THRESH_BINARY)
    
    # Perform erosion 
    erosion_size = 2
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (2 * erosion_size + 1, 2 * erosion_size+1), (erosion_size, erosion_size))
    erosion_dst = cv2.erode(binary_img, element)
    
    # Detect circle using HoughCircles
    circles = cv2.HoughCircles(erosion_dst, cv2.HOUGH_GRADIENT, dp=1, minDist=frame.shape[0] / 64, param1=200, param2=10, minRadius=75, maxRadius=120)
    
    # Draw the circles detected
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1]) # center coordinates of the circle
            radius = i[2] # radius of the circle
            
            # Draw the circle center
            cv2.circle(frame, center, 1, (0, 100, 100), 3)
            # Draw the circle outline
            cv2.circle(frame, center, radius, (0, 0, 255), 3)
            
    # Display the resulting frame
    cv2.imshow('Detected Circles', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()