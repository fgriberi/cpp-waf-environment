#include <iostream>
#include <sstream>
#include <string>
#include <stdio.h>
#include <fstream>
#include "calcex.h"
#include "calculator.h"

using namespace std;

Calculator* calc;

int main(int argc, char* argv[]) {
  string line;
  string eof;
  int p=0;
  for(int i=0;i<argc; i++){
    string word =argv[i];
    if(word=="-i") p=1;
    if(word=="-c") p=2;
  }
  if (p==0){
    try{
      cout << "Please enter a calculator expression: ";
      getline(cin, line);
      calc = new Calculator();
      int result = calc->eval(line);
      cout << "The result is " << result << endl;
      delete calc;
    }
    catch(Exception ex) {
      cout << "Program Aborted due to exception!" << endl;
    }
  }
  if(p==1){
    cout << "Please enter a calculator expression: " << endl;
    cout << ">";
    while(getline(cin,line)){
      if(line == "eof" || line =="EOF"){
	break;
      }else{
      try {
	calc = new Calculator();
	int result = calc->eval(line);
	cout << "The result is " << result << endl;
	cout << ">";
	delete calc;
      }
      catch(Exception ex) {
	cout << "Parser error!" << endl;
	cout << ">";
      }
      }
    }
  }
  if(p==2){
    try {
      cout << "Please enter a calculator expression: " << endl;
      cout << ">";
      getline(cin, line);
      calc = new Calculator();
      string result = calc ->codigoEwe(line);
      ofstream archivo;
      archivo.open("a.ewe");
      archivo << "#The result is:\n#Inicia raiz\nmain: sp := 5 \n      uno := 1\n      tres := 3 \n      sp := sp + uno \n" << result << "\n#Fin raiz \n     sp:= sp - uno \n     tmp := M[sp+1] \nwriteInt(tmp) \nhalt \nequ tmp    M[0] \nequ tmp2   M[1] \nequ uno    M[2] \nequ tres   M[3] \nequ mem    M[4]\nequ sp     M[5] \nequ stack  M[6] \n" << endl;
      archivo.close();
      cout << "Su archivo .ewe se ha creado exitosamente, por favor busquelo en la carpeta en la que se encuentra actualmente" <<endl;
      delete calc;
    }catch (Exception exc){
      cout << "Program Aborted due to Exception!" << endl;
    }
  }
}
