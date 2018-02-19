package kaimere.real.optimization.general

import kaimere.real.objects.{Function, RealVector}
import OptimizationAlgorithm.Area
import kaimere.real.optimization.classic.zero_order.RandomSearch
import kaimere.real.optimization.general.instructions.Instruction
import kaimere.real.optimization.metaheuristic._
import kaimere.real.optimization.classic.zero_order.RandomSearch.RS_State._
import kaimere.real.optimization.general.MetaOptimizationAlgorithm.MOA_State._
import kaimere.real.optimization.general.initializers.Initializer
import kaimere.real.optimization.metaheuristic.SimulatedAnnealing.SA_State._
import kaimere.real.optimization.metaheuristic.ExplosionSearch.ES_State._
import kaimere.real.optimization.metaheuristic.CatSwarmOptimization.CSO_State._
import kaimere.tools.etc._
import spray.json._

abstract class OptimizationAlgorithm {

  var f: Function = null
  var area: Area = null
  var currentState: State = null

  def initialize(f: Function, area: Area, state: Option[Vector[Map[String, Double]]] = None, initializer: Initializer = null): Unit = {
    this.f = f
    this.area = area
    this.currentState =
      (if (state.isEmpty) initializer.generateState(this)
      else state.get) |> initializeFromGivenState
  }

  def initializeFromGivenState(state: Vector[Map[String, Double]]): State

  def iterate(): Unit

  def work(instruction: Instruction): RealVector = {
    instruction.reset()
    while(instruction.continue(this))
      iterate()
    instruction.onQuit(this)
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
      case "HS" | "hs" | "HarmonySearch" => HarmonySearch(csv)
      case _ => throw DeserializationException("Unsupported Algorithm")
    }
  }

  def toJson(algorithm: OptimizationAlgorithm): JsValue = {
    algorithm match {
      case rs: RandomSearch => rs.toJson
      case sa: SimulatedAnnealing => sa.toJson
      case cso: CatSwarmOptimization => cso.toJson
      case es: ExplosionSearch => es.toJson
      case hs: HarmonySearch => hs.toJson
      case moa: MetaOptimizationAlgorithm => moa.toJson
      case _ => throw new Exception("Unsupported Algorithm")
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
          case "HarmonySearch" => json.convertTo[HarmonySearch]
          case "MetaOptimizationAlgorithm" => json.convertTo[MetaOptimizationAlgorithm]
          case _ => throw DeserializationException("Unsupported Algorithm")
        }
      case _ => throw DeserializationException("OptimizationAlgorithm expected")
    }
  }

}
