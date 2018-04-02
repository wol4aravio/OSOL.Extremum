package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Optimization.Nodes.GeneralNode

final class Algorithm[Base, FuncType, V <: Optimizable[Base, FuncType]]
(nodes: Seq[GeneralNode[Base, FuncType, V]], transitionMatrix: Seq[(Int, Option[Int], Int)]) {

  private var state: State[Base, FuncType, V] = new State()

  private var currentNode: GeneralNode[Base, FuncType, V] = null

  def initialize(f: Map[String, FuncType] => FuncType, area: Area): Unit = {
    nodes.foreach(_.initialize(f, area, state))
    currentNode = nodes.head
  }

  def work(f: Map[String, FuncType] => FuncType, area: Area): V = {
    initialize(f, area)
    while (true) {
      currentNode.process(f, area, state)
      val currentConditionValue = currentNode.getCurrentCondition(f, area, state)
      val nextNode = transitionMatrix.find { case (currentId, condition, _) =>
        currentId == currentNode.nodeId && condition == currentConditionValue }
      if (nextNode.isDefined) { currentNode = nodes.find(_.nodeId == nextNode.get._3).get }
      else return state.result.get
    }
    state.result.get
  }

}
