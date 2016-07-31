#include <algorithm>
#include <opencv2/opencv.hpp>

#define ull unsigned long long int 

using namespace cv;
using namespace std;

const int blur_radius = 31;
const int thresh = 41;

ull dct_hash(Mat &image) {
    Mat resized_image, dct_image;

    resize(image, resized_image, Size(32,32));
    resized_image.convertTo(resized_image, CV_32F);
    dct(resized_image, dct_image);

    float sum = 0;
    float* row;
    for (int i = 0; i < 8; ++i) {
        row = dct_image.ptr<float>(i);
        for (int j = 0; j < 8; ++j) {
            sum += row[j];
        }
    }
    sum -= dct_image.at<float>(Point(0,0));

    float average = sum / 63.f;
    ull hash = 0;
    for (int i = 0; i < 8; ++i) {
        row = dct_image.ptr<float>(i);
        for (int j = 0; j < 8; ++j) {
            hash = (hash << 1) | (row[j] > average);
        }
    }    

    return hash;
}

bool point_cmp_by_x(Point pt1, Point pt2) {
    return pt1.x > pt2.x;
}

void crop(Mat &image) {
    Mat image_copy = image.clone();
    vector< vector<Point> > contours;
    int height = image.rows; 
    int width = image.cols;

    blur(image_copy, image_copy, Size(blur_radius,blur_radius));
    threshold(image_copy, image_copy, thresh, 255, THRESH_BINARY);
    findContours(image_copy, contours, RETR_LIST, CHAIN_APPROX_SIMPLE);

    int i = 0;
    int area_threshold = height * width / 4;
    while (i < contours.size()) {
        vector<Point> cnt = contours[i];
        if (int(contourArea(cnt)) < area_threshold) {
            contours.erase(contours.begin() + i);
        } else {
            ++i;
        }
    }

    Point center = Point(height, width);
    vector <Point> frame_contour;
    for (vector< vector<Point> >::iterator cnt = contours.begin(); cnt != contours.end(); ++cnt) {
        if (pointPolygonTest(*cnt, center, false)) {
            frame_contour = *cnt;
            break;
        }        
    }
    
    if (frame_contour.size() == 0) {
        cerr << "Frame contour could not be found." << endl;
        return;
    }

    RotatedRect frame_rect = minAreaRect(frame_contour);
    Point2f vertices[4];
    frame_rect.points(vertices);
    float offset = float(blur_radius) / 2;

    Size2f cropped_size = frame_rect.size;
    if (frame_rect.angle < -45.f) {
        cropped_size = Size2f(cropped_size.height, cropped_size.width);
    }

    sort(vertices, vertices + 4, point_cmp_by_x); 
    if (vertices[0].y > vertices[1].y) {
        Point temp(vertices[0]);
        vertices[0] = vertices[1];
        vertices[1] = temp;
    }
    if (vertices[2].y < vertices[3].y) {
        Point temp(vertices[2]);
        vertices[2] = vertices[3];
        vertices[3] = temp;
    }

    vertices[0].x -= offset;
    vertices[0].y += offset;
    vertices[1].x -= offset;
    vertices[1].y -= offset;
    vertices[2].x += offset;
    vertices[2].y -= offset;

    Point2f target_corners[3] =  { Point(cropped_size.width-1,0), Point(cropped_size.width-1,cropped_size.height-1), Point(0,cropped_size.height-1) };
    Mat trans_mat = getAffineTransform(vertices, target_corners);
    warpAffine(image, image, trans_mat, cropped_size);
}

int main(int argc, char **argv) {
    /* code */
    return 0;
}
