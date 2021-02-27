#include <iostream>
#include <string>
#include <vector>



int main()  {
  std::string command;
  std::string name;
  std::vector<std::string> list;
  unsigned int j=0;
  std::cout << "Commands: ADD, PRINT, REMOVE, QUIT" << std::endl;

  while(j==0) {
    std::cout << "Enter a command:" << std::endl;
    std::cin >> command;

    if(command=="ADD")  {
      std::cout << "Enter a name:" << std::endl;
      std::cin >> name;
      list.push_back(name);
      std::cout << "Number of names in the vector: " << std::endl
      << list.size() << std::endl;
    }

    else if(command=="PRINT") {
      for(unsigned int i=0;i<list.size();i++) {
        std::cout << list[i] << std::endl;
      }
    }

      else if(command=="REMOVE")  {
        std::cout << "Removing the last element:" << std::endl
        << list[list.size()-1] << std::endl;
        list.erase(list.begin()+(list.size()-1));
      }

      else if(command=="QUIT")  {
        j=1;
      }
    }
  return 0;
}
