import time
import numpy as np
import cv2
points_list = []
green_select = []
points_select = []
pin_center = []

def load_image(cap):
    return cap.read()[1]

def main():
    # cap = cv2.VideoCapture(0)
    # time.sleep(2)  # Allow time for the camera to warm up

    # while True:
    new_image_path = 'out2/image23.jpg' # E 30  # C 20
    # image = load_image(new_image_path)
    image = cv2.imread(new_image_path)
    if image is None:
        raise ValueError("Error: Could not open the newly uploaded image.")
    
    # Converting the image into gray-scale
    image = cv2.cvtColor(image, cv2.COLOR_BAYER_BG2BGR)
    cv2.imshow(image)
    # Finding edges of the image
    edge_image = cv2.Canny(image, 250, 200)
    # if image is not None:
    #     adjusted_contour_frame, adjusted_num_pins, shape, classify_found = refine_pin_detection_adjusted(image)
    #     cv2.imshow('Refined Pin Detection', adjusted_contour_frame) 

    #     print(classify_found)

    key = cv2.waitKey(1)
    if key == ord('q'):  # Press 'q' to exit the loop
        cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    main()
    
# Load the new image

# # Display the result
# cv2.namedWindow('Refined Contours', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Refined Contours', shape[0], shape[1])  # Resize window to 1300x600 pixels
# cv2.imshow('Refined Contours', adjusted_contour_frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # Save the result
# adjusted_output_path = '/mnt/data/AdjustedRefinedContourPin_image_with_boxes.png'
# cv2.imwrite(adjusted_output_path, adjusted_contour_frame)

# adjusted_output_path, adjusted_num_pins
