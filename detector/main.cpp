#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/objdetect/objdetect.hpp>

int main(int argc, char** argv) {
  using namespace std;
  cv::Mat src_img = cv::imread(argv[1], 1);
  string cascade_file = "./" + string(argv[2]);
  cv::CascadeClassifier cascade;
  cout << "cascade file: " << cascade_file << endl;
  cascade.load(cascade_file);
  if(cascade.empty()) {
    cerr << "cannot load cascade file" << endl;
    exit(-1);
  }
  vector<cv::Rect> objects;
  cascade.detectMultiScale(src_img, objects, 1.1, 3, 0, cv::Size(12, 40));
  vector<cv::Rect>::const_iterator iter = objects.begin();
  cout << "count: " << objects.size() << endl;
  while(iter!=objects.end()) {
    cv::rectangle(src_img,
                  cv::Rect(iter->x, iter->y, iter->width, iter->height),
                  cv::Scalar(0, 0, 255), 4);
    ++iter;
  }
  cv::imwrite("box/detect.jpg", src_img);
  return 0;
}
