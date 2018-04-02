package OSOL.Extremum.Core.Scala.Optimization.Nodes

import OSOL.Extremum.Core.Scala.Optimization._
import OSOL.Extremum.Core.Scala.Optimization.Exceptions._

class TerminationViaMaxIterations[Base, FuncType, V <: Optimizable[Base, FuncType]](val maxIteration: Int, val nextNodeId: Int, override val nodeId: Int)
  extends GeneralNode[Base, FuncType, V ](nodeId) {

  final private val parameterName = "currentIteration"

  final override def initialize(f: Map[String, FuncType] => FuncType, area: Area, s: State[Base, FuncType, V]): Unit = {
    try {
      val _ = s.getParameter[Int](parameterName)
      throw new ParameterAlreadyExistsException(parameterName)
    }
    catch {
      case _: NoSuchParameterException => s.setParameter(parameterName, 0)
      case _ => throw new Exception("Unknown Exception")
    }
  }

  final override def process(f: Map[String, FuncType] => FuncType, area: Area, s: State[Base, FuncType, V]): Unit = {
    s.setParameter(parameterName, s.getParameter[Int](parameterName) + 1)
  }

  final override def getCurrentCondition(f: Map[String, FuncType] => FuncType, area: Area, s: State[Base, FuncType, V]): Option[Int] = {
    if (s.getParameter[Int](parameterName) > maxIteration) Some(-1)
    else Some(nextNodeId)
  }

}
