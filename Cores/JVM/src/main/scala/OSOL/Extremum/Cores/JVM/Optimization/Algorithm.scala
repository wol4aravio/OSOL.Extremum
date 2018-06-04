package OSOL.Extremum.Cores.JVM.Optimization

import OSOL.Extremum.Cores.JVM.Optimization.Nodes.GeneralNode
import spray.json._
import java.io.{File, FileWriter}

import OSOL.Extremum.Cores.JVM.Optimization

final class Algorithm[Base, FuncType, V <: Optimizable[Base, FuncType]]
(nodes: Seq[GeneralNode[Base, FuncType, V]], transitionMatrix: Seq[(java.lang.Integer, Option[java.lang.Integer], java.lang.Integer)]) {

  private var state: State[Base, FuncType, V] = new State()

  private var currentNode: GeneralNode[Base, FuncType, V] = null

  def reset(): Unit = {
    state = new State()
    currentNode = null
  }

  def initialize(f: Map[String, FuncType] => FuncType, area: Area): Unit = {
    nodes.foreach(_.initialize(f, area, state))
    currentNode = nodes.head
  }

  def work(f: Map[String, FuncType] => FuncType, area: Area, logStates: Option[String] = None): V = {
    val logger = new Optimization.Algorithm.Logger[Base, FuncType, V](logStates)
    logger.initialize()

    initialize(f, area)
    logger(state)
    var continue = true
    while (continue) {
      currentNode.process(f, area, state)
      logger(state)
      val currentConditionValue = currentNode.getCurrentCondition(f, area, state)
      val nextNode = transitionMatrix.find { case (currentId, condition, _) =>
        currentId == currentNode.nodeId && condition == currentConditionValue }
      if (nextNode.isDefined) { currentNode = nodes.find(_.nodeId == nextNode.get._3).get }
      else { continue = false }
    }
    logger(state)
    state.result.get
  }

  def serializeState(): JsValue = this.state.toJson()

}

object Algorithm {

  case class Logger[Base, FuncType, V <: Optimizable[Base, FuncType]](logLocation: Option[String]) {

    var counter = 1

    def purgeFolder(file: File): Unit = {
      if (file.isDirectory) file.listFiles.foreach(purgeFolder)
      if (file.exists && !file.delete) throw new Exception(s"Unable to delete ${file.getAbsolutePath}")
    }

    def initialize(): Unit = {
      if (logLocation.isDefined) {
        val location = new File(logLocation.get)
        if (location.exists()) purgeFolder(location)
        else location.mkdir()
      }
    }

    def apply(state: State[Base, FuncType, V]): Unit ={
      if (logLocation.isDefined){
        val printer = new FileWriter(s"${logLocation.get}/$counter.json")
        printer.write(state.toJson().prettyPrint)
        printer.close()
        counter += 1
      }
    }
  }

}
