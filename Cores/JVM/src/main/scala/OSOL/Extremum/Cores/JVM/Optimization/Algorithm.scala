package OSOL.Extremum.Cores.JVM.Optimization

import OSOL.Extremum.Cores.JVM.Optimization.Nodes.GeneralNode
import OSOL.Extremum.Cores.JVM.Optimization.Nodes.GeneralNode
import spray.json.JsValue

/** Algorithm that is constructed on steps (aka nodes) and transition matrix
  *
  * @param nodes algorithm's steps
  * @param transitionMatrix rules of transition between nodes
  * @tparam Base base type of `V` element
  * @tparam FuncType type of target function
  * @tparam V type of element on which optimization will be performed
  * @example `Algorithm[RealVector, Double, RealVector`
  * @example `Algorithm[IntervalVector, Interval, IntervalVector]`
  */
final class Algorithm[Base, FuncType, V <: Optimizable[Base, FuncType]]
(nodes: Seq[GeneralNode[Base, FuncType, V]], transitionMatrix: Seq[(Int, Option[Int], Int)]) {

  /** Holds current [[OSOL.Extremum.Cores.JVM.Optimization.State State]] */
  private var state: State[Base, FuncType, V] = new State()

  /** Holds current [[GeneralNode Node]] */
  private var currentNode: GeneralNode[Base, FuncType, V] = null

  /** Resets current algorithm */
  def reset(): Unit = {
    state = new State()
    currentNode = null
  }

  /** Initialization phase
    *
    * @param f target function
    * @param area search area
    */
  def initialize(f: Map[String, FuncType] => FuncType, area: Area): Unit = {
    nodes.foreach(_.initialize(f, area, state))
    currentNode = nodes.head
  }

  /** Run algorithm
    *
    * @param f target function
    * @param area search area
    * @return `V` on which minimum value is reached
    */
  def work(f: Map[String, FuncType] => FuncType, area: Area): V = {
    initialize(f, area)
    var continue = true
    while (continue) {
      currentNode.process(f, area, state)
      val currentConditionValue = currentNode.getCurrentCondition(f, area, state)
      val nextNode = transitionMatrix.find { case (currentId, condition, _) =>
        currentId == currentNode.nodeId && condition == currentConditionValue }
      if (nextNode.isDefined) { currentNode = nodes.find(_.nodeId == nextNode.get._3).get }
      else { continue = false }
    }
    state.result.get
  }

  /** Serializes current state */
  def serializeState(): JsValue = this.state.toJson()

}
