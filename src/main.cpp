// MyExecRefsLib.cpp
// compile with: cl /EHsc MyExecRefsLib.cpp /link MathFuncsLib.lib

#include <iostream>
#include "mathFuncs.h"

int main()
{
    double a = 7.4;
    int b = 99;

    std::cout << "a + b = " << NSMaths::MathFuncs::add(a, b) << std::endl;
    std::cout << "a - b = " << NSMaths::MathFuncs::subtract(a, b) << std::endl;
    std::cout << "a * b = " << NSMaths::MathFuncs::multiply(a, b) << std::endl;
    std::cout << "a / b = " << NSMaths::MathFuncs::divide(a, b) << std::endl;
    return 0;
}

//g++ src/main.cpp src/mathFuncs.cpp -I include/