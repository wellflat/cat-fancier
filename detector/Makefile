CXX = g++
CXXFLAGS = -g -Wall `pkg-config --cflags opencv`
#CXXFLAGS = `pkg-config --cflags opencv`
#LDFLAGS = `pkg-config --libs opencv`
LDFLAGS = -L/usr/local/opencv-2.4.7/lib -lopencv_core -lopencv_highgui -lopencv_objdetect -lopencv_imgproc
TARGET = main
SOURCE = main.cpp

TARGET:
	$(CXX) -o $(TARGET) $(SOURCE) $(CXXFLAGS) $(LDFLAGS)

.PHONY: clean
clean:
	rm -f *.o *~ $(TARGET)
