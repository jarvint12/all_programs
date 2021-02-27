#include <iostream>
#include <vector>


int GetMin(const std::vector<int>& v)  {
  double smallest = v[0];
  for (unsigned int i=1;i<v.size();i++) {
    if (smallest>v[i])  {
      smallest=v[i];
    }
  }
  return smallest;
}

int GetMax(const std::vector<int>& v)  {
  double largest = v[0];
  for(unsigned int i=1;i<v.size();i++)  {
    if (v[i]>largest)
      largest = v[i];
  }
  return largest;
}

double GetAverage(const std::vector<int>& v)  {
  int sum=0;
  double j=0;
  for(unsigned int i=0;i<v.size();i++)  {
    sum+=v[i];
    j++;
  }
  return sum/j;
}


int main()  {
  std::vector<int> numbers = {10, 15, 1};
  std::cout << "Smallest value: " << GetMin(numbers) << std::endl
  << "Largest value: " << GetMax(numbers) << std::endl
  << "Average value: " << GetAverage(numbers) << std::endl;
  return 0;
}
