package kaimere.real.optimization.general

import kaimere.real.objects.{Function, RealVector}
import kaimere.real.objects.RealVector._
import kaimere.real.optimization.Helper
import kaimere.real.optimization.classic.zero_order.RandomSearch.RS_State
import kaimere.real.optimization.general.MetaOptimizationAlgorithm.MOA_State
import kaimere.real.optimization.metaheuristic.CatSwarmOptimization.{CSO_State, Cat}
import kaimere.real.optimization.metaheuristic.ExplosionSearch.{Bomb, ES_State}
import kaimere.real.optimization.metaheuristic.SimulatedAnnealing.SA_State
import kaimere.real.optimization.metaheuristic._
import kaimere.tools.etc._
import spray.json._

trait State {

  def toVectors(): Vector[RealVector]

  def getBestBy(f: Function): (RealVector, Double)

}

object State {

  def toJson(state: State): JsValue = JsObject("vectors" -> JsArray(state.toVectors().map(_.toJson)))

  def fromJson(json: JsValue, f: Function, targetAlgorithm: String, parameters: Map[String, Object] = Map(), targetArea: Option[OptimizationAlgorithm.Area] = None): State = {
    val Seq(vectorArray) = json.asJsObject.getFields("vectors")
    vectorArray match {
      case JsArray(array) =>
        val vectors = array.map(_.convertTo[RealVector].vals)
        val area =
          if (targetArea.isEmpty) vectors.head.keys.map(key => (key, (Double.NegativeInfinity, Double.PositiveInfinity))).toMap[String, (Double, Double)]
          else targetArea.get
        targetAlgorithm match {
          case "RandomSearch" | "rs" | "RS" | "RS_State" => {
            val realVectors = Helper.prepareInitialState(vectors)
            val bestVector = Helper.chooseOneBest(realVectors, f)
            (bestVector, f(bestVector)) |> RS_State.tupled
          }
          case "SimulatedAnnealing" | "sa" | "SA" | "SA_State" => {
            val realVectors = Helper.prepareInitialState(vectors)
            val bestVector = Helper.chooseOneBest(realVectors, f)
            (bestVector, f(bestVector), 0) |> SA_State.tupled
          }
          case "CatSwarmOptimization" | "cso" | "CSO" | "CSO_State" => {
            val realVectors = Helper.prepareInitialState(vectors)
            val bestVectors = Helper.chooseSeveralBest(realVectors, f, parameters("numberOfCats").asInstanceOf[Int])
            bestVectors.map(v => Cat.createRandomCat(v, f, area, parameters("maxVelocity").asInstanceOf[Map[String, (Double, Double)]])) |> CSO_State
          }
          case "ExposionSearch" | "es" | "ES" | "ES_State" => {
            val realVectors = Helper.prepareInitialState(vectors)
            val bestVectors = Helper.chooseSeveralBest(realVectors, f, parameters("numberOfBombs").asInstanceOf[Int])
            bestVectors.map(v => Bomb(v, f(v))).sortBy(_.fitness) |> ES_State
          }
          case "MetaOptimizationAlgorithm" | "moa" | "MOA" | "MOA_State" => {
            val realVectors = Helper.prepareInitialState(vectors)
            val bestVector = Helper.chooseOneBest(realVectors, f)
            MOA_State(bestVector)
          }
        case _ => throw DeserializationException("State Expected")
      }

    }
  }

}