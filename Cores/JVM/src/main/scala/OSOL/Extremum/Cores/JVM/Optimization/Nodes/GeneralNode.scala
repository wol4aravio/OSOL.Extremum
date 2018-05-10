package OSOL.Extremum.Cores.JVM.Optimization.Nodes

import OSOL.Extremum.Cores.JVM.Optimization._

abstract class GeneralNode[Base, FuncType, V <: Optimizable[Base, FuncType]](val nodeId: java.lang.Integer) {

  def initialize(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit

  def process(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Unit

  def getCurrentCondition(f: Map[String, FuncType] => FuncType, area: Area, state: State[Base, FuncType, V]): Option[java.lang.Integer] = None

}
