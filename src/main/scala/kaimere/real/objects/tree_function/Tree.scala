package kaimere.real.objects.tree_function

import kaimere.real.objects.RealVector

import math._

trait Tree {

  def eval(vector: RealVector): Double

}

object Tree {

  class AdditionTree(left: Tree, right: Tree) extends Tree {

    override def eval(vector: RealVector): Double = left.eval(vector) + right.eval(vector)

  }

  class SubtractionTree(left: Tree, right: Tree) extends Tree {

    override def eval(vector: RealVector): Double = left.eval(vector) - right.eval(vector)

  }

  class MultiplicationTree(left: Tree, right: Tree) extends Tree {

    override def eval(vector: RealVector): Double = left.eval(vector) * right.eval(vector)

  }

  class DivisionTree(left: Tree, right: Tree) extends Tree {

    override def eval(vector: RealVector): Double = left.eval(vector) / right.eval(vector)

  }

  class PowerTree(left: Tree, right: Tree) extends Tree {

    override def eval(vector: RealVector): Double = pow(left.eval(vector), right.eval(vector))

  }

  class NegTree(subTree: Tree) extends Tree {

    override def eval(vector: RealVector): Double = -subTree.eval(vector)

  }

  class SinTree(subTree: Tree) extends Tree {

    override def eval(vector: RealVector): Double = sin(subTree.eval(vector))

  }

  class CosTree(subTree: Tree) extends Tree {

    override def eval(vector: RealVector): Double = cos(subTree.eval(vector))

  }

  class ExpTree(subTree: Tree) extends Tree {

    override def eval(vector: RealVector): Double = exp(subTree.eval(vector))

  }

  class AbsTree(subTree: Tree) extends Tree {

    override def eval(vector: RealVector): Double = abs(subTree.eval(vector))

  }

  class LnTree(subTree: Tree) extends Tree {

    override def eval(vector: RealVector): Double = log(subTree.eval(vector))

  }

  class SqrtTree(subTree: Tree) extends Tree {

    override def eval(vector: RealVector): Double = sqrt(subTree.eval(vector))

  }

  class ConstantTree(value: Double) extends Tree {

    override def eval(vector: RealVector): Double = value

  }

  class VariableTree(varName: String) extends Tree {

    override def eval(vector: RealVector): Double = vector(varName)

  }

}