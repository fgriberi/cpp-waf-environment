#ifndef calculator_h
#define calculator_h

#include <string>
 
using namespace std;


class Calculator {
 public:
   Calculator();

   int eval(string expr);
   string codigoEwe(string expr);
   void store(int val);
   int recall();

 private:
   int memory;
};

extern Calculator* calc;

#endif

