package OSOL.Extremum.Core.Scala.Optimization.Nodes

import OSOL.Extremum.Core.Scala.Optimization._

/** Template for node definition
  *
  * @param nodeId id of the node
  * @tparam Base type of atomic element of `V`
  * @tparam FuncType required function type
  * @tparam V type of basic object
  */
abstract class GeneralNode[Base, FuncType, V <: Optimizable[Base, FuncType]](val nodeId: Int) {

  /** Initialization procedure
    *
    * @param f function to be optimized
    * @param area area on which the search will be performed
    * @param state
    */
  def initialize(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit

  /** How to process current state
    *
    * @param f function to be optimized
    * @param area area on which the search will be performed
    * @param state
    */
  def process(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit

  /** Get current condition identifier (change only for condition nodes)
    *
    * @param f function to be optimized
    * @param area area on which the search will be performed
    * @param state
    * @return current condition identifier
    */
  def getCurrentCondition(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Option[Int] = None

}
