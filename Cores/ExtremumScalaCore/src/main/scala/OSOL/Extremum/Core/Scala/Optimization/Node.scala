package OSOL.Extremum.Core.Scala.Optimization

trait Node[Base, FuncType, V <: Optimizable[Base, FuncType]] {

  def process(s: State[Base, FuncType, V]): Unit

  def getNextNode(s: State[Base, FuncType, V]): Option[Int] = None

}
