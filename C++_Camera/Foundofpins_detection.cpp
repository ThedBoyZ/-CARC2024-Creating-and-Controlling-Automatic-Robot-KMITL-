// #include <opencv2/opencv.hpp>
// #include <vector>

// using namespace cv;
// using namespace std;

// int main() {
//     // Read the image
//     Mat img = imread("/home/eaglesoft/Downloads/Screenshot (58).png");
//     if (img.empty()) {
//         cout << "Could not open or find the image" << endl;
//         return -1;
//     }

//     // Convert to grayscale
//     Mat gray_img;
//     cvtColor(img, gray_img, COLOR_BGR2GRAY);

//     // Apply a binary threshold to the grayscale image
//     Mat binary_img;
//     double thresh = 128; // you can change this threshold value as needed
//     double maxValue = 255;
//     threshold(gray_img, binary_img, thresh, maxValue, THRESH_BINARY);

//     // Perform erosion
//     Mat erosion_dst;
//     int erosion_type = MORPH_RECT;
//     int erosion_size = 2;
//     Mat element = getStructuringElement(erosion_type,
//                                         Size(2 * erosion_size + 1, 2 * erosion_size + 1),
//                                         Point(erosion_size, erosion_size));
//     erode(binary_img, erosion_dst, element);

//     // Detect circles using HoughCircles
//     vector<Vec3f> circles;
//     HoughCircles(erosion_dst, circles, HOUGH_GRADIENT, 1, img.rows / 64, 200, 10, 75, 120);

//     // Draw the circles detected
//     for (size_t i = 0; i < circles.size(); i++) {
//         Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
//         int radius = cvRound(circles[i][2]);
//         circle(img, center, radius, Scalar(0, 0, 255), 2, 8, 0);
//     }

//     // Display the image with detected circles
//     imshow("Detected Circles", img);
//     waitKey(0);

//     return 0;
// }

#include <opencv.hpp>
#include <opencv_modules.hpp>
#include <vector>

using namespace cv;
using namespace std;

int main()
{
    // Initialize the video capture object
    VideoCapture cap(0);

    if (!cap.isOpened())
    {
        cout << "Error: Could not open video capture" << endl;
        return -1;
    }

    while (true)
    {
        Mat frame;
        // Capture frame-by-frame
        cap >> frame;

        if (frame.empty())
        {
            cout << "Error: Could not read frame" << endl;
            break;
        }

        // Convert to grayscale
        Mat gray_img;
        cvtColor(frame, gray_img, COLOR_BGR2GRAY);

        // Apply a binary threshold to the grayscale image
        Mat binary_img;
        double thresh = 128; // you can change this threshold value as needed
        double maxValue = 255;
        threshold(gray_img, binary_img, thresh, maxValue, THRESH_BINARY);

        // Perform erosion
        Mat erosion_dst;
        int erosion_type = MORPH_RECT;
        int erosion_size = 2;
        Mat element = getStructuringElement(erosion_type,
                                            Size(2 * erosion_size + 1, 2 * erosion_size + 1),
                                            Point(erosion_size, erosion_size));
        erode(binary_img, erosion_dst, element);

        // Detect circles using HoughCircles
        vector<Vec3f> circles;
        HoughCircles(erosion_dst, circles, HOUGH_GRADIENT, 1, frame.rows / 64, 200, 10, 75, 120);

        // Draw the circles detected
        for (size_t i = 0; i < circles.size(); i++)
        {
            Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
            int radius = cvRound(circles[i][2]);
            circle(frame, center, radius, Scalar(0, 0, 255), 2, 8, 0);
        }

        // Display the frame with detected circles
        imshow("Detected Circles", frame);

        // Break the loop on 'q' key press
        if (waitKey(1) == 'q')
        {
            break;
        }
    }

    // Release the capture and destroy all OpenCV windows
    cap.release();
    destroyAllWindows();

    return 0;
}
