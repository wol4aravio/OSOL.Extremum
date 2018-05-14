package OSOL.Extremum.Cores.JVM.Optimization.Nodes

import OSOL.Extremum.Cores.JVM.Optimization._
import OSOL.Extremum.Cores.JVM.Optimization.Exceptions._
import OSOL.Extremum.Cores.JVM.Optimization.{Optimizable, State}

class SetParametersNode[Base, FuncType, V <: Optimizable[Base, FuncType]]
(override val nodeId: java.lang.Integer, val parameters: Map[String, Any])
  extends GeneralNode[Base, FuncType, V ](nodeId) {

  final override def initialize(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = {
    parameters.foreach { case (k, v) => state.setParameter(k, v)}
  }

  final override def process(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = { }

}
