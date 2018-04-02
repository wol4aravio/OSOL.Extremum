package OSOL.Extremum.Core.Scala.Optimization.Nodes

import OSOL.Extremum.Core.Scala.Optimization._
import OSOL.Extremum.Core.Scala.Optimization.Exceptions._

class TerminationViaMaxIterations[Base, FuncType, V <: Optimizable[Base, FuncType]](override val nodeId: Int, val maxIteration: Int)
  extends GeneralNode[Base, FuncType, V ](nodeId) {

  final private val parameterName = "currentIteration"

  final override def initialize(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = {
    try {
      val _ = state.getParameter[Int](parameterName)
      throw new ParameterAlreadyExistsException(parameterName)
    }
    catch {
      case _: NoSuchParameterException => state.setParameter(parameterName, 0)
      case _ => throw new Exception("Unknown Exception")
    }
  }

  final override def process(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = {
    state.setParameter(parameterName, state.getParameter[Int](parameterName) + 1)
  }

  final override def getCurrentCondition(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Option[Int] = {
    if (state.getParameter[Int](parameterName) > maxIteration) Some(1)
    else Some(0)
  }

}
