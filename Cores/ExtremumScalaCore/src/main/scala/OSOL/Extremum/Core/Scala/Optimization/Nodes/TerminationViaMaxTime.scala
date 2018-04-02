package OSOL.Extremum.Core.Scala.Optimization.Nodes

import OSOL.Extremum.Core.Scala.Optimization._
import OSOL.Extremum.Core.Scala.Optimization.Exceptions._

class TerminationViaMaxTime[Base, FuncType, V <: Optimizable[Base, FuncType]](override val nodeId: Int, val maxTime: Double)
  extends GeneralNode[Base, FuncType, V ](nodeId) {

  final private val parameterName = "startTime"

  final override def initialize(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = {
    try {
      val _ = state.getParameter[Long](parameterName)
      throw new ParameterAlreadyExistsException(parameterName)
    }
    catch {
      case _: NoSuchParameterException => state.setParameter(parameterName, System.nanoTime())
      case _ => throw new Exception("Unknown Exception")
    }
  }

  final override def process(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit = { }

  final override def getCurrentCondition(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Option[Int] = {
    if (1e-9 * (System.nanoTime() - state.getParameter[Long](parameterName)) > maxTime) Some(1)
    else Some(0)
  }

}
