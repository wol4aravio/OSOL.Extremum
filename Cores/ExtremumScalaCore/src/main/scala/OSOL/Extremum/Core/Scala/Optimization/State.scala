package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Optimization.Exceptions._

/** This class represents arbitrary state of an algorithm
  *
  * @tparam Base base type of `V` element
  * @tparam FuncType type of target function
  * @tparam V type of element on which optimization will be performed
  * @example `State[RealVector, Double, RealVector`
  * @example `State[IntervalVector, Interval, IntervalVector]`
  */
class State[Base, FuncType, V <: Optimizable[Base, FuncType]] {

  /** Variable that will contain final result */
  var result: Option[V] = None

  /** Variable that will contain arbitrary parameters introduced by user */
  final private val parameters: scala.collection.mutable.Map[String, Any] = scala.collection.mutable.Map.empty[String, Any]

  /** Set parameter value
    *
    * @param name parameter name
    * @param value target value
    * @tparam T parameter type
    */
  def setParameter[T <: Any](name: String, value: T): Unit = parameters(name) = value

  /** Access parameter by name
    *
    * @param name parameter name
    * @tparam T its type
    * @return its value
    */
  def getParameter[T <: Any](name: String): T = {
    if (parameters.contains(name)) parameters(name).asInstanceOf[T]
    else throw new NoSuchParameterException(name)
  }

}
