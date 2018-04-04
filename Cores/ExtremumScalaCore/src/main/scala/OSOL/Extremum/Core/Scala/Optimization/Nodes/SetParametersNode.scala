package OSOL.Extremum.Core.Scala.Optimization.Nodes

import OSOL.Extremum.Core.Scala.Optimization._
import OSOL.Extremum.Core.Scala.Optimization.Exceptions._

class SetParametersNode[Base, FuncType, V <: Optimizable[Base, FuncType]]
(override val nodeId: Int, val parameters: Map[String, Any])
  extends GeneralNode[Base, FuncType, V ](nodeId) {

  final override def initialize(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = {
    parameters.foreach { case (k, v) => state.setParameter(k, v)}
  }

  final override def process(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = { }

}
