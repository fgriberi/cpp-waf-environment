#include "ast.h"
#include <iostream>
#include <sstream>
#include "calculator.h"

// for debug information uncomment
// #define debug

AST::AST() {}

AST::~AST() {}

BinaryNode::BinaryNode(AST* left, AST* right):
   AST(),
   leftTree(left),
   rightTree(right)
{}

BinaryNode::~BinaryNode() {
#ifdef debug
   cout << "In BinaryNode destructor" << endl;
#endif

   try {
      delete leftTree;
   } catch (...) {}

   try {
      delete rightTree;
   } catch(...) {}
}
   
AST* BinaryNode::getLeftSubTree() const {
   return leftTree;
}

AST* BinaryNode::getRightSubTree() const {
   return rightTree;
}

UnaryNode::UnaryNode(AST* sub):
   AST(),
   subTree(sub)
{}

UnaryNode::~UnaryNode() {
#ifdef debug
   cout << "In UnaryNode destructor" << endl;
#endif

   try {
      delete subTree;
   } catch (...) {}
}
   
AST* UnaryNode::getSubTree() const {
   return subTree;
}

AddNode::AddNode(AST* left, AST* right):
   BinaryNode(left,right)
{}

int AddNode::evaluate() {
   return getLeftSubTree()->evaluate() + getRightSubTree()->evaluate();
}

string AddNode::ewe() {
  return "#Inicio de la raiz \n#Inicia AddNode \n     sp := sp + tres \n#Invocar hijo izquierdo \n" + getLeftSubTree()->ewe() + "#Termina hijo izquierdo \n     sp := sp - tres \n     tmp := M[sp+3] \n     M[sp+1] := tmp \n     sp := sp + tres \n#Invocar hijo derecho \n" + getRightSubTree()->ewe() + "#Termina hijo derecho \n     sp := sp -tres \n     tmp := M[sp+3] \n     M[sp+2] := tmp \n     tmp := M[sp+1] \n     tmp2 := M[sp+2] \n     tmp := tmp + tmp2 \n     M[sp+0] := tmp \n#Fin AddNode \n#Fin invocar raiz";
}

SubNode::SubNode(AST* left, AST* right):
   BinaryNode(left,right)
{}

int SubNode::evaluate() {
   return getLeftSubTree()->evaluate() - getRightSubTree()->evaluate();
}

string SubNode::ewe() {
  return "#Inicia SubNode \n     sp := sp + tres \n#Invocar hijo izquierdo \n" + getLeftSubTree()->ewe() + "Termina hijo izquierdo \n     sp := sp - tres \n     tmp := M[sp+3] \n     M[sp+1] := tmp \n     sp := sp + tres \n#Invocar hijo derecho \n" + getRightSubTree()->ewe() + "#Termina hijo derecho \n     sp := sp - tres \n     tmp := M[sp+3] \n     M[sp+2] := tmp \n tmp := M[sp+1] \n     tmp2 := M[sp+2] \n     tmp := tmp - tmp2 \n     M[sp+0] := tmp \n#Fin SubNode \n     sp := sp -uno \n     tmp := M[sp+1] \n     writeInt(tmp) \n     halt";
}

MultNode::MultNode(AST* left, AST* right):
  BinaryNode(left,right)
{}

int MultNode::evaluate() {
  return getLeftSubTree()->evaluate() * getRightSubTree()->evaluate();
}

string MultNode::ewe() {
  return "#Inicia MultNode \n     sp := sp + tres \n#Invocar hijo izquierdo \n" + getLeftSubTree()->ewe() + "#Termina hijo izquierdo \n     sp := sp-tres \n     tmp := M[sp+3] \n     M[sp+1] := tmp \n     sp := sp + tres \n#Invocar hijo derecho \n" + getRightSubTree()->ewe() + "#Termina hijo derecho \n     sp := sp -tres \n     tmp := M[sp+3] \n     M[sp+2] := tmp \n     tmp := M[sp+1] \n     tmp2 := M[sp+2] \n     tmp := tmp * tmp2 \n     M[sp+0] := tmp \n#Fin MultNode";
}

DivNode::DivNode(AST* left, AST* right):
  BinaryNode(left,right)
{}

int DivNode::evaluate() {
  return getLeftSubTree()->evaluate() / getRightSubTree()->evaluate();
}

string DivNode::ewe() {
  return "#Inicia DivNode \n     sp := sp + tres \n#Invocar hijo izquierdo \n" + getLeftSubTree()->ewe() + "#Termina hijo izquierdo \n     sp := sp - tres \n     tmp := M[sp+3] \n     M[sp+1] := tmp \n     sp := sp + tres \n#Invocar hijo derecho \n" + getRightSubTree()->ewe() + "#Termina hijo derecho \n     sp := sp - tres \n     tmp := M[sp+3] \n     M[sp+2] := tmp \n     tmp := M[sp+1] \n     tmp2 := M[sp+2] \n     tmp := tmp / tmp2 \n     M[sp+0] := tmp \n#Fin DivNode";
}

NumNode::NumNode(int n) :
   AST(),
   val(n)
{}

int NumNode::evaluate() {
   return val;
}

string NumNode::ewe() {
  stringstream mg;
  mg << val;
  string palabra; 
  palabra = mg.str();
  return "#Inicio NumNode \n     tmp := " + palabra + "\n     M[sp+0] := tmp \n#Fin NumNode \n";
}

StoreNode::StoreNode(AST *sub)
  : UnaryNode(sub) {}

int StoreNode::evaluate(){
  int tmp;
  tmp = getSubTree()->evaluate();
  calc->store(tmp);
  return tmp;
}

string StoreNode::ewe(){
  return "#Inicio StoreNode \n     sp := sp + uno \n#Invocar hijo StoreNode \n" + getSubTree()->ewe() + "#Fin hijo StoreNode \n     sp := sp - uno \n     tmp := M[sp+1] \n     M[sp+0] := tmp \n     mem := tmp \n#Fin StoreNode\n";
}

RecallNode::RecallNode() : AST() {}

int RecallNode:: evaluate(){
  return calc->recall();
}

string RecallNode::ewe(){
  return "#Inicio RecallNode \n     M[sp+0] := mem \n#Fin RecallNode\n";
}
