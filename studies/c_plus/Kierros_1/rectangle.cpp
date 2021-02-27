#include <iostream>

int main()  {
  int width;
  int height;
  std::cout << "Please enter width and height" << std::endl;
  std::cin >> width;
  std::cin >> height;
  int area = width*height;
  int circumference = 2*width+2*height;
  std::cout << "Area: " << area << std::endl;
  std::cout << "Circumference: " << circumference << std::endl;
  return 0;
}
