package OSOL.Extremum.Cores.JVM.Optimization.Nodes

import OSOL.Extremum.Cores.JVM.Optimization._
import OSOL.Extremum.Cores.JVM.Optimization.Exceptions._

class TerminationViaMaxTime[Base, FuncType, V <: Optimizable[Base, FuncType]]
(override val nodeId: java.lang.Integer, val maxTime: java.lang.Double, parameterName: String = "startTime")
  extends GeneralNode[Base, FuncType, V ](nodeId) {

  final override def initialize(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = {
    try {
      val _ = state.getParameter[java.lang.Long](parameterName)
      throw new ParameterAlreadyExistsException(parameterName)
    }
    catch {
      case _: NoSuchParameterException => state.setParameter(parameterName, System.nanoTime())
      case _ => throw new ParameterAlreadyExistsException(parameterName)
    }
  }

  final override def process(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = { }

  final override def getCurrentCondition(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Option[java.lang.Integer] = {
    if (1e-9 * (System.nanoTime() - state.getParameter[java.lang.Long](parameterName)) > maxTime) Some(1)
    else Some(0)
  }

}
