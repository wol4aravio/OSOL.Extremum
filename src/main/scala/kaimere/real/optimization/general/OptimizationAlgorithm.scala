package kaimere.real.optimization.general

import kaimere.real.objects.{Function, RealVector}
import OptimizationAlgorithm.Area
import OptimizationAlgorithm.MergeStrategy.MergeStrategy
import kaimere.real.optimization.classic.zero_order.RandomSearch
import kaimere.real.optimization.metaheuristic._
import spray.json._

abstract class OptimizationAlgorithm {

  protected var f: Function = null
  protected var area: Area = null
  protected var currentState: State = null

  def initialize(f: Function, area: Area, state: Vector[Map[String, Double]], mergeStrategy: MergeStrategy): Unit = {
    this.f = f
    this.area = area
    this.currentState = merge(state, mergeStrategy)
  }

  def merge(state: Vector[Map[String, Double]], mergeStrategy: MergeStrategy): State

  def iterate(): Unit

  final def work(instruction: Instruction): RealVector = {
    instruction.reset()
    while(instruction.continue())
      iterate()
    currentState.getBestBy(f)
  }

}

object OptimizationAlgorithm {

  type Area = Map[String, (Double, Double)]

  object MergeStrategy extends Enumeration {
    type MergeStrategy = Value
    val force = Value
    val selfInit = Value
  }

  def fromJson(json: JsValue): OptimizationAlgorithm = {
    json.asJsObject.getFields("name") match {
      case Seq(JsString(name)) =>
        name match {
          case "RandomSearch" => json.convertTo[RandomSearch]
          case "SimulatedAnnealing" => json.convertTo[SimulatedAnnealing]
          case "CatSwarmOptimization" => json.convertTo[CatSwarmOptimization]
          case _ => throw DeserializationException("Unsupported Algorithm")
        }
      case _ => throw DeserializationException("OptimizationAlgorithm expected")
    }
  }

}
