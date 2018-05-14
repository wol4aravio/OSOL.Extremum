package OSOL.Extremum.Cores.JVM.Optimization.Nodes

import OSOL.Extremum.Cores.JVM.Optimization._
import OSOL.Extremum.Cores.JVM.Optimization.Exceptions._

class TerminationViaMaxIterations[Base, FuncType, V <: Optimizable[Base, FuncType]]
(override val nodeId: java.lang.Integer, val maxIteration: java.lang.Integer, parameterName: String = "currentIteration")
  extends GeneralNode[Base, FuncType, V ](nodeId) {

  final override def initialize(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = {
    var value: Option[java.lang.Integer] = None
    try { value = Some(state.getParameter[java.lang.Integer](parameterName)) }
    catch { case _: NoSuchParameterException => state.setParameter(parameterName, 0) }
    finally {  if (value.isDefined) throw new ParameterAlreadyExistsException(parameterName) }
  }

  final override def process(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = {
    state.setParameter(parameterName, state.getParameter[java.lang.Integer](parameterName) + 1)
  }

  final override def getCurrentCondition(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Option[java.lang.Integer] = {
    if (state.getParameter[java.lang.Integer](parameterName) > maxIteration) Some(1)
    else Some(0)
  }

}
