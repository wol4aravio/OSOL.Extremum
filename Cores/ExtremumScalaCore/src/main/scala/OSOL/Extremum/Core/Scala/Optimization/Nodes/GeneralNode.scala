package OSOL.Extremum.Core.Scala.Optimization.Nodes

import OSOL.Extremum.Core.Scala.Optimization._

abstract class GeneralNode[Base, FuncType, V <: Optimizable[Base, FuncType]](val nodeId: Int) {

  def initialize(f: Map[String, FuncType] => FuncType, area: Area, s: State[Base, FuncType, V]): Unit

  def process(f: Map[String, FuncType] => FuncType, area: Area, s: State[Base, FuncType, V]): Unit

  def getCurrentCondition(f: Map[String, FuncType] => FuncType, area: Area, s: State[Base, FuncType, V]): Option[Int] = None

}
