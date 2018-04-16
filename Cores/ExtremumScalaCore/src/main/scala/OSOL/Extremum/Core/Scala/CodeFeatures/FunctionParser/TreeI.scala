package OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser

import OSOL.Extremum.Core.Scala.Arithmetics.Interval

abstract class TreeI {

  def calculate(values: Map[String, Interval]): Interval

}

object TreeI {

  abstract class BinaryOpTreeI(left: TreeI, right: TreeI, op: (Interval, Interval) => Interval) extends TreeI {
    final override def calculate(values: Map[String, Interval]): Interval = op(left.calculate(values), right.calculate(values))
  }

  abstract class UnaryOpTree(subTree: TreeI, op: Interval => Interval) extends TreeI {
    final override def calculate(values: Map[String, Interval]): Interval = op(subTree.calculate(values))
  }

  class AdditionTree(left: TreeI, right: TreeI) extends BinaryOpTreeI(left, right, (x, y) => x + y)

  class SubtractionTree(left: TreeI, right: TreeI) extends BinaryOpTreeI(left, right, (x, y) => x - y)

  class MultiplicationTree(left: TreeI, right: TreeI) extends BinaryOpTreeI(left, right, (x, y) => x * y)

  class DivisionTree(left: TreeI, right: TreeI) extends BinaryOpTreeI(left, right, (x, y) => x / y)

  class PowerTree(left: TreeI, right: TreeI) extends BinaryOpTreeI(left, right, (x, y) => x ** y)

  class NegTree(subTree: TreeI) extends UnaryOpTree(subTree, x => -x)

  class SinTree(subTree: TreeI) extends UnaryOpTree(subTree, x => x.sin())

  class CosTree(subTree: TreeI) extends UnaryOpTree(subTree, x => x.cos())

  class ExpTree(subTree: TreeI) extends UnaryOpTree(subTree, x => x.exp())

  class AbsTree(subTree: TreeI) extends UnaryOpTree(subTree, x => x.abs())

  class LnTree(subTree: TreeI) extends UnaryOpTree(subTree, x => x.ln())

  class SqrtTree(subTree: TreeI) extends UnaryOpTree(subTree, x => x.sqrt())

  class ConstantTree(value: Interval) extends TreeI {
    final override def calculate(values: Map[String, Interval]): Interval = value
  }

  class VariableTree(varName: String) extends TreeI {
    final override def calculate(values: Map[String, Interval]): Interval = values(varName)
  }

}