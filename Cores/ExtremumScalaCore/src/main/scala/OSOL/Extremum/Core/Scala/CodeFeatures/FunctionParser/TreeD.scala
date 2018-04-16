package OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser

abstract class TreeD {

  def calculate(values: Map[String, Double]): Double

}

object TreeD {

  abstract class BinaryOpTreeD(left: TreeD, right: TreeD, op: (Double, Double) => Double) extends TreeD {
    final override def calculate(values: Map[String, Double]): Double = op(left.calculate(values), right.calculate(values))
  }

  abstract class UnaryOpTree(subTree: TreeD, op: Double => Double) extends TreeD {
    final override def calculate(values: Map[String, Double]): Double = op(subTree.calculate(values))
  }

  class AdditionTree(left: TreeD, right: TreeD) extends BinaryOpTreeD(left, right, (x, y) => x + y)

  class SubtractionTree(left: TreeD, right: TreeD) extends BinaryOpTreeD(left, right, (x, y) => x - y)

  class MultiplicationTree(left: TreeD, right: TreeD) extends BinaryOpTreeD(left, right, (x, y) => x * y)

  class DivisionTree(left: TreeD, right: TreeD) extends BinaryOpTreeD(left, right, (x, y) => x / y)

  class PowerTree(left: TreeD, right: TreeD) extends BinaryOpTreeD(left, right, (x, y) => math.pow(x, y))

  class NegTree(subTree: TreeD) extends UnaryOpTree(subTree, x => -x)

  class SinTree(subTree: TreeD) extends UnaryOpTree(subTree, x => math.sin(x))

  class CosTree(subTree: TreeD) extends UnaryOpTree(subTree, x => math.cos(x))

  class ExpTree(subTree: TreeD) extends UnaryOpTree(subTree, x => math.exp(x))

  class AbsTree(subTree: TreeD) extends UnaryOpTree(subTree, x => math.abs(x))

  class LnTree(subTree: TreeD) extends UnaryOpTree(subTree, x => math.log(x))

  class SqrtTree(subTree: TreeD) extends UnaryOpTree(subTree, x => math.sqrt(x))

  class ConstantTree(value: Double) extends TreeD {
    final override def calculate(values: Map[String, Double]): Double = value
  }

  class VariableTree(varName: String) extends TreeD {
    final override def calculate(values: Map[String, Double]): Double = values(varName)
  }

}