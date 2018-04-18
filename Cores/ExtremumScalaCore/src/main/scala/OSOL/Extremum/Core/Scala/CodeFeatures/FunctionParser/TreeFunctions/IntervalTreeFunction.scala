package OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser.TreeFunctions

import OSOL.Extremum.Core.Scala.Arithmetics.Interval
import OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser.Parser
import OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser.Trees.Tree
import OSOL.Extremum.Core.Scala.Vectors.IntervalVector

class IntervalTreeFunction(t: Tree[Interval]) {
  def apply(v: IntervalVector): Interval = t.calculate(v)
}

object IntervalTreeFunction {
  def apply(str: String): IntervalTreeFunction = new IntervalTreeFunction(Parser.parseToIntervalTree(str))
}