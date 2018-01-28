package kaimere.real.optimization.metaheuristic

import kaimere.real.optimization.general._
import kaimere.real.objects.{Function, RealVector}
import kaimere.real.objects.RealVector._
import kaimere.real.optimization.metaheuristic.ExplosionSearch.{Bomb, ES_State}
import kaimere.tools.random.GoRN
import kaimere.tools.etc._
import spray.json._

case class ExplosionSearch(numberOfBombs: Int, powerRatio: Double, dimensions: Int)
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
    val idsChosen = GoRN.getFromSeries(state.indices, numberOfBombs, withReturn = true)
    idsChosen.map(id => Bomb(state(id), f(state(id)))).sortBy(_.fitness) |> ES_State
  }

  override def initialize(f: Function, area: OptimizationAlgorithm.Area,
                          state: Option[Vector[Map[String, Double]]]): Unit = {
    powerDistribution = calculatePowerDistribution(area)
    super.initialize(f, area, state)
  }

  override def iterate(): Unit = {
    val ES_State(bombs) = currentState
    val newBombs = Range(0, numberOfBombs).map(id => bombs(id).explode(powerDistribution(id), f, area, dimensions))
    currentState = newBombs.foldLeft(Seq.empty[Bomb]){ case (seq, (b_1, b_2)) =>
      b_2 +: (b_1 +: seq) }.sortBy(_.fitness).take(numberOfBombs) |> ES_State
  }

}

object ExplosionSearch {

  private case class Bomb(location: RealVector, fitness: Double) {

    def explode(power: Map[String, Double], f: Function, area: OptimizationAlgorithm.Area, numberOfDimensions: Int): (Bomb, Bomb) = {

      val explodingKeys = GoRN.getFromSeries(power.keys.toSeq, numberOfDimensions, withReturn = false).toSet
      val remainingKeys = power.keySet -- explodingKeys

      val delta = remainingKeys.map(key => (key, (-power(key), power(key)))).toMap[String, (Double, Double)]
      val deltaLeft = explodingKeys.map(key => (key, (-power(key), 0.0))).toMap[String, (Double, Double)] ++ delta
      val deltaRight = explodingKeys.map(key => (key, (0.0, power(key)))).toMap[String, (Double, Double)] ++ delta

      val bomb_1 = location.moveBy(GoRN.getContinuousUniform(deltaLeft)).constrain(area)
      val bomb_2 = location.moveBy(GoRN.getContinuousUniform(deltaLeft)).constrain(area)

      (Bomb(bomb_1, f(bomb_1)), Bomb(bomb_2, f(bomb_2)))

    }

  }

  private case class ES_State(bombs: Seq[Bomb]) extends State  {

    override def toVectors(): Vector[RealVector] = bombs.map(_.location).toVector

    def getBestBy(f: Function): RealVector = bombs.minBy(_.fitness).location

    def apply(id: Int): Bomb = bombs(id)

  }

  implicit object ExplosionSearchJsonFormat extends RootJsonFormat[ExplosionSearch] {
    def write(es: ExplosionSearch) =
      JsObject(
        "name" -> JsString("ExplosionSearch"),
        "numberOfBombs" -> JsNumber(es.numberOfBombs),
        "powerRatio" -> JsNumber(es.powerRatio),
        "dimensions" -> JsNumber(es.dimensions))

    def read(json: JsValue): ExplosionSearch =
      json.asJsObject.getFields("name", "numberOfBombs", "powerRatio", "dimensions") match {
        case Seq(JsString(name), JsNumber(numberOfBombs), JsNumber(powerRatio), JsNumber(dimensions)) =>
          if (name != "ExplosionSearch") throw DeserializationException("ExplosionSearch expected")
          else ExplosionSearch(numberOfBombs.toInt, powerRatio.toDouble, dimensions.toInt)
        case _ => throw DeserializationException("ExplosionSearch expected")
      }
  }

}