package kaimere.real.optimization.classic.zero_order

import kaimere.real.optimization.general._
import kaimere.real.optimization.general.OptimizationAlgorithm.MergeStrategy
import kaimere.real.optimization.general.OptimizationAlgorithm.MergeStrategy.MergeStrategy
import kaimere.real.objects.{RealVector, Function}
import kaimere.tools.random.GoRN
import kaimere.tools.etc._

import spray.json._

case class RandomSearch(numberOfAttempts: Int, deltaRatio: Double) extends OptimizationAlgorithm {

  private var possibleDelta: Map[String, (Double, Double)] = Map.empty

  override def merge(state: Vector[Map[String, Double]], mergeStrategy: MergeStrategy): State = {
    mergeStrategy match {
      case MergeStrategy.force =>
        val realVectors = state.map(x => x.map { case (key, value) => (key, value)}).map(RealVector.fromMap)
        Vector(State(realVectors).getBestBy(f)) |> State.apply
      case _ => throw new Exception(s"Unsupported merge strategy $mergeStrategy")
    }
  }

  override def initialize(f: Function, area: OptimizationAlgorithm.Area,
                          state: Vector[Map[String, Double]], mergeStrategy: MergeStrategy): Unit = {
    super.initialize(f, area, state, mergeStrategy)
    possibleDelta = this.area.map { case (key, value) =>
      val width: Double = value._2 - value._1
      (key, (-deltaRatio * width, deltaRatio * width))
    }
  }

  override def iterate(): Unit = {
    val currentPoint: RealVector = currentState(0)
    val newPoints: State = (1 to numberOfAttempts)
      .map { _ =>
        val delta: RealVector = GoRN.getContinuousUniform(possibleDelta) |> RealVector.apply
        (currentPoint + delta).constrain(area)
      }.toVector |> State.apply
    currentState = Vector(newPoints.getBestBy(f)) |> State.apply
  }

}

object RandomSearch {

  implicit object RandomSearchJsonFormat extends RootJsonFormat[RandomSearch] {
    def write(rs: RandomSearch) =
      JsObject(
        "name" -> JsString("RandomSearch"),
        "numberOfAttempts" -> JsNumber(rs.numberOfAttempts),
        "deltaRatio" -> JsNumber(rs.deltaRatio))

    def read(json: JsValue): RandomSearch =
      json.asJsObject.getFields("name", "numberOfAttempts", "deltaRatio") match {
        case Seq(JsString(name), JsNumber(numberOfAttempts), JsNumber(deltaRatio)) =>
          if (name != "RandomSearch") throw DeserializationException("RandomSearch expected")
          else RandomSearch(numberOfAttempts.toInt, deltaRatio.toDouble)
        case _ => throw DeserializationException("RandomSearch expected")
      }
  }

}