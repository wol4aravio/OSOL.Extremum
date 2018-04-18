package OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser.TreeFunctions

import OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser.Parser
import OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser.Trees.Tree
import OSOL.Extremum.Cores.JVM.Vectors.RealVector

class DoubleTreeFunction(t: Tree[Double]) {
  def apply(v: RealVector): Double = t.calculate(v)
}

object DoubleTreeFunction {
  def apply(str: String): DoubleTreeFunction = new DoubleTreeFunction(Parser.parseToDoubleTree(str))
}