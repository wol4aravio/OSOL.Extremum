package OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser.TreeFunctions

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser.Parser
import OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser.Trees.Tree
import OSOL.Extremum.Cores.JVM.Vectors.IntervalVector

class IntervalTreeFunction(t: Tree[Interval]) {
  def apply(v: IntervalVector): Interval = t.calculate(v)
}

object IntervalTreeFunction {
  def apply(str: String): IntervalTreeFunction = new IntervalTreeFunction(Parser.parseToIntervalTree(str))
}