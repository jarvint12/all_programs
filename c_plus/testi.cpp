#include <iostream>
#include <string>

class Mammal {
public:
    Mammal(double weight) : weight_(weight) { }
    double GetWeight() { return weight_; }

private:
    double weight_;
};

class Dog : public Mammal   {
public:
    Dog(std::string& name, double weight) : Mammal(weight) {
        sound_ = "Wuff!";
        name_ = name;
    }

    std::string& MakeSound()    {
    return sound_;
}

private:
    std::string name_;
    std::string sound_;
};

class Cat : public Mammal   {
public:
    Cat(std::string& name, double weight) : Mammal(weight) {
        sound_ = "Meow";
        name_ = name;
    }

    std::string& MakeSound()    {
    return sound_;
}

private:
    std::string name_;
    std::string sound_;

};




int main(void) {
    Mammal m(10.5);
    std::cout << "Mammal's weight is " << m.GetWeight() << std::endl;

    Dog ransu("Ransu", 23.1);
    std::cout << ransu.GetName() << " weighs " << ransu.GetWeight()
	      << " and says: " << ransu.MakeSound() << std::endl;
    if (dynamic_cast< Mammal* >(&ransu)) {
	    std::cout << ransu.GetName() << " is a Mammal" << std::endl;
    }

    Cat garfield("Garfield", 16.5);
    std::cout << garfield.GetName() << " weighs " << garfield.GetWeight()
	      << " and says: " << garfield.MakeSound() << std::endl;
    if (dynamic_cast< Mammal* >(&garfield)) {
	    std::cout << garfield.GetName() << " is a Mammal" << std::endl;
    }

    std::cout << "In fact, all dogs say " << Dog::MakeSound() << std::endl;
}
