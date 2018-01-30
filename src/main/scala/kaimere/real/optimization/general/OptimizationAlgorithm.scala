package kaimere.real.optimization.general

import kaimere.real.objects.{Function, RealVector}
import OptimizationAlgorithm.Area
import kaimere.real.optimization.classic.zero_order.RandomSearch
import kaimere.real.optimization.metaheuristic._
import spray.json._

abstract class OptimizationAlgorithm {

  var f: Function = null
  var area: Area = null
  var currentState: State = null

  def initialize(f: Function, area: Area, state: Option[Vector[Map[String, Double]]] = None): Unit = {
    this.f = f
    this.area = area
    this.currentState =
      if (state.isEmpty) initializeRandomState()
      else initializeFromGivenState(state.get)
  }

  def initializeRandomState(): State

  def initializeFromGivenState(state: Vector[Map[String, Double]]): State

  def iterate(): Unit

  def work(instruction: Instruction): RealVector = {
    instruction.reset()
    while(instruction.continue())
      iterate()
    currentState.getBestBy(f)._1
  }

}

object OptimizationAlgorithm {

  type Area = Map[String, (Double, Double)]

  def fromCsv(csv: String): OptimizationAlgorithm = {
    val name = csv.split(",").head
    name match {
      case "RS" | "rs" | "RandomSearch" => RandomSearch(csv)
      case "SA" | "sa" | "SimulatedAnnealing" => SimulatedAnnealing(csv)
      case "CSO" | "cso" | "CatSwarmOptimization" => CatSwarmOptimization(csv)
      case "ES" | "es" | "ExplosionSearch" => ExplosionSearch(csv)
      case _ => throw DeserializationException("Unsupported Algorithm")
    }
  }

  def fromJson(json: JsValue): OptimizationAlgorithm = {
    json.asJsObject.getFields("name") match {
      case Seq(JsString(name)) =>
        name match {
          case "RandomSearch" => json.convertTo[RandomSearch]
          case "SimulatedAnnealing" => json.convertTo[SimulatedAnnealing]
          case "CatSwarmOptimization" => json.convertTo[CatSwarmOptimization]
          case "ExplosionSearch" => json.convertTo[ExplosionSearch]
          case _ => throw DeserializationException("Unsupported Algorithm")
        }
      case _ => throw DeserializationException("OptimizationAlgorithm expected")
    }
  }

}
