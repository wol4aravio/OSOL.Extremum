package OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser

import OSOL.Extremum.Core.Scala.Vectors.VectorObject

object TreeD {

  abstract class BinaryOpTree[Double](left: Tree[Double], right: Tree[Double], op: (Double, Double) => Double) extends Tree[Double] {
    final override def calculate(v: VectorObject[Double]): Double = op(left.calculate(v), right.calculate(v))
  }

  abstract class UnaryOpTree[Double](subTree: Tree[Double], op: Double => Double) extends Tree[Double] {
    final override def calculate(v: VectorObject[Double]): Double = op(subTree.calculate(v))
  }

  class AdditionTree(left: Tree[Double], right: Tree[Double]) extends BinaryOpTree[Double](left, right, (x, y) => x + y)

  class SubtractionTree(left: Tree[Double], right: Tree[Double]) extends BinaryOpTree[Double](left, right, (x, y) => x - y)

  class MultiplicationTree(left: Tree[Double], right: Tree[Double]) extends BinaryOpTree[Double](left, right, (x, y) => x * y)

  class DivisionTree(left: Tree[Double], right: Tree[Double]) extends BinaryOpTree[Double](left, right, (x, y) => x / y)

  class PowerTree(left: Tree[Double], right: Tree[Double]) extends BinaryOpTree[Double](left, right, (x, y) => math.pow(x, y))

  class NegTree(subTree: Tree[Double]) extends UnaryOpTree[Double](subTree, x => -x)

  class SinTree(subTree: Tree[Double]) extends UnaryOpTree[Double](subTree, x => math.sin(x))

  class CosTree(subTree: Tree[Double]) extends UnaryOpTree[Double](subTree, x => math.cos(x))

  class ExpTree(subTree: Tree[Double]) extends UnaryOpTree[Double](subTree, x => math.exp(x))

  class AbsTree(subTree: Tree[Double]) extends UnaryOpTree[Double](subTree, x => math.abs(x))

  class LnTree(subTree: Tree[Double]) extends UnaryOpTree[Double](subTree, x => math.log(x))

  class SqrtTree(subTree: Tree[Double]) extends UnaryOpTree[Double](subTree, x => math.sqrt(x))

  class ConstantTree(value: Double) extends Tree[Double] {
    final override def calculate(v: VectorObject[Double]): Double = value
  }

  class VariableTree(varName: String) extends Tree[Double] {
    final override def calculate(v: VectorObject[Double]): Double = v(varName)
  }

}