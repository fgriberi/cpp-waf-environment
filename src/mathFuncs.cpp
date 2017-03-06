/**
 * @brief mathFuncs.cpp
 */

#include "mathFuncs.h"

namespace NSMaths
{

double MathFuncs::add(double a, double b)
{
    return a + b;
}

double MathFuncs::subtract(double a, double b)
{
    return a - b;
}

double MathFuncs::multiply(double a, double b)
{
    return a * b;
}

double MathFuncs::divide(double a, double b)
{
    return a / b;
}

double MathFuncs::mean(double a, double b)
{
	return (a+b) / 2;
}

} //end namespace