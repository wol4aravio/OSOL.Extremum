package kaimere.real.optimization.metaheuristic

import kaimere.real.optimization._
import kaimere.real.optimization.general._
import kaimere.real.objects.{Function, RealVector}
import kaimere.real.optimization.general.initializers.Initializer
import kaimere.tools.random.GoRN
import kaimere.tools.etc._
import spray.json._

case class ExplosionSearch(numberOfBombs: Int, powerRatio: Double, numberOfDims: Int)
  extends OptimizationAlgorithm {

  case class Bomb(location: RealVector, fitness: Double) {

    def explode(power: Map[String, Double], f: Function, area: OptimizationAlgorithm.Area): (Bomb, Bomb) = {

      val explodingKeys = GoRN.getFromSeries(
        power.keys.toSeq,
        if (numberOfDims < 0) area.size else numberOfDims,
        withReturn = false)

      val remainingKeys = power.keySet -- explodingKeys

      val delta = explodingKeys.map(key => (key, (-power(key), power(key)))).toMap[String, (Double, Double)] ++
        remainingKeys.map(key => (key, (0.0, 0.0))).toMap[String, (Double, Double)]

      val bomb_1 = location.moveBy(GoRN.getContinuousUniform(delta)).constrain(area)
      val bomb_2 = location.moveBy(GoRN.getContinuousUniform(delta)).constrain(area)

      (Bomb(bomb_1, f(bomb_1)), Bomb(bomb_2, f(bomb_2)))

    }

  }

  case class ES_State(bombs: Seq[Bomb]) extends State(vectors = bombs.map(_.location).toVector) {

    override def getBestBy(f: Function): (RealVector, Double) = (bombs.head.location, bombs.head.fitness)

  }

  private var powerDistribution: Map[Int, Map[String, Double]] = Map.empty

  private def calculatePowerDistribution(area: OptimizationAlgorithm.Area): Map[Int, Map[String, Double]] = {
    Range(0, numberOfBombs)
      .map { id =>
        (id, area.map { case (key, (min, max)) => (key, id * powerRatio * (max - min) / (numberOfBombs - 1)) })
      }.toMap
  }

  override def initializeFromGivenState(state: State): State = {
    val realVectors = Helper.prepareInitialState(state)
    val bestVectors = Helper.chooseSeveralBest(realVectors, f, numberOfBombs)
    bestVectors.map(v => Bomb(v, f(v))).sortBy(_.fitness) |> ES_State.apply
  }

  override def initialize(f: Function, area: OptimizationAlgorithm.Area,
                          state: Option[State], initializer: Initializer): Unit = {
    powerDistribution = calculatePowerDistribution(area)
    super.initialize(f, area, state, initializer)
  }

  override def iterate(): Unit = {
    val ES_State(bombs) = currentState
    val newBombs = Range(0, numberOfBombs).map(id => bombs(id).explode(powerDistribution(id), f, area))
    currentState = newBombs.foldLeft(Seq.empty[Bomb]){ case (seq, (b_1, b_2)) =>
      b_2 +: (b_1 +: seq) }.sortBy(_.fitness).take(numberOfBombs) |> ES_State.apply
  }

}

object ExplosionSearch {

  def apply(csv: String): ExplosionSearch = {
    val Array(name, numberOfBombs, powerRatio, numberOfDims) = csv.split(",")
    name match {
      case "ES" | "es" | "ExplosionSearch" => ExplosionSearch(numberOfBombs.toInt, powerRatio.toDouble, numberOfDims.toInt)
      case _ => throw DeserializationException("ExplosionSearch expected")
    }
  }

  implicit object ExplosionSearchJsonFormat extends RootJsonFormat[ExplosionSearch] {
    def write(es: ExplosionSearch) =
      JsObject(
        "name" -> JsString("ExplosionSearch"),
        "numberOfBombs" -> JsNumber(es.numberOfBombs),
        "powerRatio" -> JsNumber(es.powerRatio),
        "numberOfDims" -> JsNumber(es.numberOfDims)
      )

    def read(json: JsValue): ExplosionSearch =
      json.asJsObject.getFields("name", "numberOfBombs", "powerRatio", "numberOfDims") match {
        case Seq(JsString(name), JsNumber(numberOfBombs), JsNumber(powerRatio), JsNumber(numberOfDims)) =>
          if (name != "ExplosionSearch") throw DeserializationException("ExplosionSearch expected")
          else ExplosionSearch(Seq(name, numberOfBombs, powerRatio, numberOfDims).mkString(","))
        case _ => throw DeserializationException("ExplosionSearch expected")
      }
  }

}