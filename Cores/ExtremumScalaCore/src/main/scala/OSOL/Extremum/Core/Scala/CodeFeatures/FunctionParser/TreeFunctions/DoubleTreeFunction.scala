package OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser.TreeFunctions

import OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser.Parser
import OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser.Trees.Tree
import OSOL.Extremum.Core.Scala.Vectors.RealVector

class DoubleTreeFunction(t: Tree[Double]) {
  def apply(v: RealVector): Double = t.calculate(v)
}

object DoubleTreeFunction {
  def apply(str: String): DoubleTreeFunction = new DoubleTreeFunction(Parser.parseToDoubleTree(str))
}