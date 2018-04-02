package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Optimization.Exceptions._

class State[Base, FuncType, V <: Optimizable[Base, FuncType]] {

  var result: Option[V] = None

  final private val parameters: scala.collection.mutable.Map[String, Any] = scala.collection.mutable.Map.empty[String, Any]

  def setParameter[T <: Any](name: String, value: T): Unit = parameters(name) = value

  def getParameter[T <: Any](name: String): T = {
    if (parameters.contains(name)) parameters(name).asInstanceOf[T]
    else throw new NoSuchParameterException(name)
  }

}
