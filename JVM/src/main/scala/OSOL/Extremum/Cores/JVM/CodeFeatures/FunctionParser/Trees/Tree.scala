package OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser.Trees

import OSOL.Extremum.Cores.JVM.Vectors.VectorObject
import OSOL.Extremum.Cores.JVM.Vectors.VectorObject

abstract class Tree[T] {
  def calculate(v: VectorObject[T]): T
}

object Tree {
  abstract class BinaryOpTree[T](left: Tree[T], right: Tree[T], op: (T, T) => T) extends Tree[T] {
    final override def calculate(v: VectorObject[T]): T = op(left.calculate(v), right.calculate(v))
  }

  abstract class UnaryOpTree[T](subTree: Tree[T], op: T => T) extends Tree[T] {
    final override def calculate(v: VectorObject[T]): T = op(subTree.calculate(v))
  }
}