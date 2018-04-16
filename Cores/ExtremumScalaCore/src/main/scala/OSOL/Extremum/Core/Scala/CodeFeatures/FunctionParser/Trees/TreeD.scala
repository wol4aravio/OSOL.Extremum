package OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser.Trees

import OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser.Trees.Tree._
import OSOL.Extremum.Core.Scala.Vectors.VectorObject

object TreeD {

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