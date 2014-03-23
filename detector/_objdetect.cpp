#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/objdetect/objdetect.hpp>

int main(int argc, char** argv) {
  using namespace std;
  if(argc != 3) {
    cerr << "./_objdetect [image file] [cascade file]" << endl;
    exit(-1);
  }
  cv::Mat src_img = cv::imread(argv[1], 1);
  if(src_img.empty()) {
    cerr << "cannot load image" << endl;
    exit(-1);
  }
  cv::Mat dst_img = src_img.clone();
  string cascade_file = string(argv[2]);
  cv::CascadeClassifier cascade;
  cout << "cascade file: " << cascade_file << endl;
  cascade.load(cascade_file);
  if(cascade.empty()) {
    cerr << "cannot load cascade file" << endl;
    exit(-1);
  }
  vector<cv::Rect> objects;
  cascade.detectMultiScale(src_img, objects, 1.1, 3);
  vector<cv::Rect>::const_iterator iter = objects.begin();
  cout << "count: " << objects.size() << endl;
  while(iter!=objects.end()) {
    cout << "(x, y, width, height) = (" << iter->x << ", " << iter->y << ", "
         << iter->width << ", " << iter->height << ")" << endl;
    cv::rectangle(dst_img,
                  cv::Rect(iter->x, iter->y, iter->width, iter->height),
                  cv::Scalar(0, 0, 255), 2);
    ++iter;
  }
  cv::imwrite("box/detect.jpg", dst_img);
  return 0;
}
