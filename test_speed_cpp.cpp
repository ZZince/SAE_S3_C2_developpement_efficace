#include <iostream>
#include <opencv2/opencv.hpp>

std::tuple<int, int, int, int, int, int> searchPoints(const cv::Mat &imageGray, int threshold, int numColumns) {
    int height = imageGray.rows;
    int width = imageGray.cols;

    // Find the point without stars on the left side of the grayscale image
    int leftX;
    for (int x = 0; x < numColumns; ++x) {
        for (int y = 0; y < height; ++y) {
            if (imageGray.at<uchar>(y, x) <= threshold) {
                leftX = x;
                break;
            }
        }
    }

    // Find the point without stars at the 1/3 of the grayscale image
    int oneThirdX = width / 3;
    int oneThirdY;
    for (int y = 0; y < height; ++y) {
        if (imageGray.at<uchar>(y, oneThirdX) <= threshold) {
            oneThirdY = y;
            break;
        }
    }

    // Find the point without stars at the 2/3 of the grayscale image
    int twoThirdsX = 2 * (width / 3);
    int twoThirdsY;
    for (int y = 0; y < height; ++y) {
        if (imageGray.at<uchar>(y, twoThirdsX) <= threshold) {
            twoThirdsY = y;
            break;
        }
    }

    // Find the point without stars on the right side of the grayscale image
    int rightX;
    for (int x = width - 1; x > width - numColumns - 1; --x) {
        for (int y = 0; y < height; ++y) {
            if (imageGray.at<uchar>(y, x) <= threshold) {
                rightX = x;
                break;
            }
        }
    }

    return std::make_tuple(leftX, oneThirdX, oneThirdY, twoThirdsX, twoThirdsY, rightX);
}


cv::Mat generateLinearGradient(const cv::Mat &imageColor, int leftX, int oneThirdX, int oneThirdY, int twoThirdsX, int twoThirdsY, int rightX) {
    cv::Mat gradientLinear = cv::Mat::zeros(imageColor.size(), imageColor.type());

    cv::Vec3b colorPixelLeft = imageColor.at<cv::Vec3b>(0, leftX);
    cv::Vec3b colorPixelOneThird = imageColor.at<cv::Vec3b>(oneThirdY, oneThirdX);
    cv::Vec3b colorPixelTwoThirds = imageColor.at<cv::Vec3b>(twoThirdsY, twoThirdsX);
    cv::Vec3b colorPixelRight = imageColor.at<cv::Vec3b>(0, rightX);

    // Calculate the ratios for the three segments
    cv::Mat ratioLeft = cv::Mat(1, oneThirdX - leftX, CV_32F);
    cv::Mat ratioMiddle = cv::Mat(1, twoThirdsX - oneThirdX, CV_32F);
    cv::Mat ratioRight = cv::Mat(1, rightX - twoThirdsX + 1, CV_32F);

    for (int i = 0; i < ratioLeft.cols; ++i) {
        ratioLeft.at<float>(0, i) = static_cast<float>(i) / (oneThirdX - leftX);
    }

    for (int i = 0; i < ratioMiddle.cols; ++i) {
        ratioMiddle.at<float>(0, i) = static_cast<float>(i) / (twoThirdsX - oneThirdX);
    }

    for (int i = 0; i < ratioRight.cols; ++i) {
        ratioRight.at<float>(0, i) = static_cast<float>(i) / (rightX - twoThirdsX);
    }

    // Interpolate colors using the ratios
    gradientLinear(cv::Rect(0, 0, oneThirdX, gradientLinear.rows)) =
        (1 - ratioLeft.t()) * colorPixelLeft + ratioLeft.t() * colorPixelOneThird;

    gradientLinear(cv::Rect(oneThirdX, 0, twoThirdsX - oneThirdX, gradientLinear.rows)) =
        (1 - ratioMiddle.t()) * colorPixelOneThird + ratioMiddle.t() * colorPixelTwoThirds;

    gradientLinear(cv::Rect(twoThirdsX, 0, rightX - twoThirdsX + 1, gradientLinear.rows)) =
        (1 - ratioRight.t()) * colorPixelTwoThirds + ratioRight.t() * colorPixelRight;

    return gradientLinear;
}

int main() {
    int leftX, oneThirdX, oneThirdY, twoThirdsX, twoThirdsY, rightX;

    std::cout << "Test for 100 gradient generation: " << std::endl;

    cv::Mat imageColor = cv::imread("gradient/Elephants_Trunk_Combined.jpg");
    cv::Mat imageGray; 
    cv::cvtColor(imageColor, imageGray, cv::COLOR_BGR2GRAY);

    double start_time = static_cast<double>(cv::getTickCount());

    for (int i = 0; i < 100; ++i) {
        //to assign multiple values
        std::tie(leftX, oneThirdX, oneThirdY, twoThirdsX, twoThirdsY, rightX) = searchPoints(imageGray, 128, 70);

        cv::Mat gradientLinear = generateLinearGradient(imageColor, leftX, oneThirdX, oneThirdY, twoThirdsX, twoThirdsY, rightX);
    }

    double end_time = static_cast<double>(cv::getTickCount());
    double elapsed_time = (end_time - start_time) / cv::getTickFrequency();

    std::cout << "Elapsed time for 100 gradient generations: " << elapsed_time << " seconds" << std::endl;

    return 0;
}
