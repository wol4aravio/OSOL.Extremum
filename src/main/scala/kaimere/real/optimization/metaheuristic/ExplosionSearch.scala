package kaimere.real.optimization.metaheuristic

import kaimere.real.optimization._
import kaimere.real.optimization.general._
import kaimere.real.objects.{Function, RealVector}
import kaimere.real.objects.RealVector._
import kaimere.real.optimization.metaheuristic.ExplosionSearch.{Bomb, ES_State}
import kaimere.tools.random.GoRN
import kaimere.tools.etc._
import spray.json._

case class ExplosionSearch(numberOfBombs: Int, powerRatio: Double)
  extends OptimizationAlgorithm {

  private var powerDistribution: Map[Int, Map[String, Double]] = Map.empty

  private def calculatePowerDistribution(area: OptimizationAlgorithm.Area): Map[Int, Map[String, Double]] = {
    Range(0, numberOfBombs)
      .map { id =>
        (id, area.map { case (key, (min, max)) =>
          (key, id * powerRatio * (max - min) / (numberOfBombs - 1))
        })
      }.toMap
  }

  override def initializeRandomState(): State = {
    (1 to numberOfBombs).map { _ =>
      val location = GoRN.getContinuousUniform(area)
      Bomb(location, f(location))
    }.sortBy(_.fitness) |> ES_State
  }

  override def initializeFromGivenState(state: Vector[Map[String, Double]]): State = {
    val realVectors = Helper.prepareInitialState(state)
    val bestVectors = Helper.chooseSeveralBest(realVectors, f, numberOfBombs)
    bestVectors.map(v => Bomb(v, f(v))).sortBy(_.fitness) |> ES_State
  }

  override def initialize(f: Function, area: OptimizationAlgorithm.Area,
                          state: Option[Vector[Map[String, Double]]]): Unit = {
    powerDistribution = calculatePowerDistribution(area)
    super.initialize(f, area, state)
  }

  override def iterate(): Unit = {
    val ES_State(bombs) = currentState
    val newBombs = Range(0, numberOfBombs).map(id => bombs(id).explode(powerDistribution(id), f, area))
    currentState = newBombs.foldLeft(Seq.empty[Bomb]){ case (seq, (b_1, b_2)) =>
      b_2 +: (b_1 +: seq) }.sortBy(_.fitness).take(numberOfBombs) |> ES_State
  }

}

object ExplosionSearch {

  case class Bomb(location: RealVector, fitness: Double) {

    def explode(power: Map[String, Double], f: Function, area: OptimizationAlgorithm.Area): (Bomb, Bomb) = {

      val Seq(explodingKey) = GoRN.getFromSeries(power.keys.toSeq, 1, withReturn = false)
      val remainingKeys = power.keySet - explodingKey

      val delta = remainingKeys.map(key => (key, (-power(key), power(key)))).toMap[String, (Double, Double)]
      val deltaLeft = delta + (explodingKey -> (-power(explodingKey), 0.0))
      val deltaRight = delta + (explodingKey -> (0.0, power(explodingKey)))

      val bomb_1 = location.moveBy(GoRN.getContinuousUniform(deltaLeft)).constrain(area)
      val bomb_2 = location.moveBy(GoRN.getContinuousUniform(deltaLeft)).constrain(area)

      (Bomb(bomb_1, f(bomb_1)), Bomb(bomb_2, f(bomb_2)))

    }

  }

  case class ES_State(bombs: Seq[Bomb]) extends State  {

    override def toVectors(): Vector[RealVector] = bombs.map(_.location).toVector

    override def getBestBy(f: Function): (RealVector, Double) = (bombs.head.location, bombs.head.fitness)

  }

  def apply(csv: String): ExplosionSearch = {
    val Array(name, numberOfBombs, powerRatio) = csv.split(",")
    name match {
      case "ES" | "es" | "ExplosionSearch" => ExplosionSearch(numberOfBombs.toInt, powerRatio.toDouble)
      case _ => throw DeserializationException("ExplosionSearch expected")
    }
  }

  implicit object ExplosionSearchJsonFormat extends RootJsonFormat[ExplosionSearch] {
    def write(es: ExplosionSearch) =
      JsObject(
        "name" -> JsString("ExplosionSearch"),
        "numberOfBombs" -> JsNumber(es.numberOfBombs),
        "powerRatio" -> JsNumber(es.powerRatio))

    def read(json: JsValue): ExplosionSearch =
      json.asJsObject.getFields("name", "numberOfBombs", "powerRatio") match {
        case Seq(JsString(name), JsNumber(numberOfBombs), JsNumber(powerRatio)) =>
          if (name != "ExplosionSearch") throw DeserializationException("ExplosionSearch expected")
          else ExplosionSearch(Seq(name, numberOfBombs, powerRatio).mkString(","))
        case _ => throw DeserializationException("ExplosionSearch expected")
      }
  }

}