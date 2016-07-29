#include <stdio.h>
#include <opencv2/opencv.hpp>
using namespace cv;

long long dct_hash(Mat &image) {
    Mat resized_image, dct_image;

    resize(image, resized_image, Size(32,32));
    resized_image.convertTo(resized_image, CV_32F);
    dct(resized_image, dct_image);

    int sum = 0;
    float* row;
    for (int i = 0; i < 8; ++i) {
        row = dct_image.ptr<float>(i);
        for (int j = 0; j < 8; ++j) {
            if (i == 0 && j == 0) continue;
            sum += row[j];
        }
    }

    float average = sum / (7*8.0);
    long long hash = 0;
    for (int i = 0; i < 8; ++i) {
        row = dct_image.ptr<float>(i);
        for (int j = 0; j < 8; ++j) {
            hash = (hash << 1) | (row[j] > average);
        }
    }    

    return hash;
}

int main(int argc, char** argv ) {
    if (argc != 2) {
        printf("usage: dct_hash <Image_Path>\n");
        return -1;
    }
    
    Mat image;
    image = imread( argv[1], CV_LOAD_IMAGE_GRAYSCALE);
    if (!image.data) {
        printf("No image data \n");
        return -1;
    }

    std::cout << dct_hash(image) << '\n';
    return 0;
}