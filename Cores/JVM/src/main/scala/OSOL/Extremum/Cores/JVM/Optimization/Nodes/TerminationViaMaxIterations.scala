package OSOL.Extremum.Cores.JVM.Optimization.Nodes

import OSOL.Extremum.Cores.JVM.Optimization._
import OSOL.Extremum.Cores.JVM.Optimization.Exceptions._

class TerminationViaMaxIterations[Base, FuncType, V <: Optimizable[Base, FuncType]]
(override val nodeId: Int, val maxIteration: Int, parameterName: String = "currentIteration")
  extends GeneralNode[Base, FuncType, V ](nodeId) {

  final override def initialize(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = {
    var value: Option[Int] = None
    try { value = Some(state.getParameter[Int](parameterName)) }
    catch { case _: NoSuchParameterException => state.setParameter(parameterName, 0) }
    finally {  if (value.isDefined) throw new ParameterAlreadyExistsException(parameterName) }
  }

  final override def process(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = {
    state.setParameter(parameterName, state.getParameter[Int](parameterName) + 1)
  }

  final override def getCurrentCondition(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Option[Int] = {
    if (state.getParameter[Int](parameterName) > maxIteration) Some(1)
    else Some(0)
  }

}
