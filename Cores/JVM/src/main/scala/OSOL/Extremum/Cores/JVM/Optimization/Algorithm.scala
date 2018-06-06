package OSOL.Extremum.Cores.JVM.Optimization

import OSOL.Extremum.Cores.JVM.Optimization.Nodes.GeneralNode
import spray.json._
import java.io.{File, FileWriter}

import OSOL.Extremum.Cores.JVM.Optimization

final class Algorithm[Base, FuncType, V <: Optimizable[Base, FuncType]]
(nodes: Seq[GeneralNode[Base, FuncType, V]], transitionMatrix: Seq[(java.lang.Integer, Option[java.lang.Integer], java.lang.Integer)]) {

  var state: State[Base, FuncType, V] = new State()

  var currentNode: GeneralNode[Base, FuncType, V] = null

  var writers: Seq[Any => JsValue] = Seq.empty

  def reset(): Unit = {
    state = new State()
    currentNode = null
  }

  def initialize(f: Map[String, FuncType] => FuncType, area: Area): Unit = {
    nodes.foreach(_.initialize(f, area, state))
    currentNode = nodes.head
  }

  def work(f: Map[String, FuncType] => FuncType, area: Area, logStates: Option[String] = None): V = {
    val logger = new Optimization.Algorithm.Logger[Base, FuncType, V](logStates, writers)
    logger.initialize()

    initialize(f, area)
    logger(state, currentNode)
    var continue = true
    while (continue) {
      currentNode.process(f, area, state)
      logger(state, currentNode)
      val currentConditionValue = currentNode.getCurrentCondition(f, area, state)
      val nextNode = transitionMatrix.find { case (currentId, condition, _) =>
        currentId == currentNode.nodeId && condition == currentConditionValue }
      if (nextNode.isDefined) { currentNode = nodes.find(_.nodeId == nextNode.get._3).get }
      else { continue = false }
    }
    logger(state, currentNode)
    state.result.get
  }

  def serializeState(): JsValue = this.state.toJson(writers)

}

object Algorithm {

  case class Logger[Base, FuncType, V <: Optimizable[Base, FuncType]](logLocation: Option[String], writers: Seq[Any => JsValue]) {

    var counter = 1

    def purgeFolder(file: File): Unit = {
      if (file.isDirectory) file.listFiles.foreach(purgeFolder)
      if (file.exists && !file.delete) throw new Exception(s"Unable to delete ${file.getAbsolutePath}")
    }

    def initialize(): Unit = {
      if (logLocation.isDefined) {
        val location = new File(logLocation.get)
        if (location.exists()) purgeFolder(location)
        location.mkdir()
      }
    }

    def apply(state: State[Base, FuncType, V], node: GeneralNode[Base, FuncType, V]): Unit ={
      if (logLocation.isDefined){
        state.setParameter("_nodeId", node.nodeId)
        val printer = new FileWriter(s"${logLocation.get}/$counter.json")
        printer.write(state.toJson(writers).prettyPrint)
        printer.close()
        counter += 1
      }
    }
  }

}
