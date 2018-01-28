package kaimere.real.optimization.classic.zero_order

import kaimere.real.optimization.general._
import kaimere.real.objects.{Function, RealVector}
import kaimere.real.optimization.classic.zero_order.RandomSearch.RS_State
import kaimere.tools.random.GoRN
import kaimere.tools.etc._
import spray.json._

case class RandomSearch(numberOfAttempts: Int, deltaRatio: Double) extends OptimizationAlgorithm {

  private var possibleDelta: Map[String, (Double, Double)] = Map.empty

  override def initializeRandomState(): State = {
    val v = GoRN.getContinuousUniform(area)
    val value = f(v)
    RS_State(v, value)
  }

  override def initializeFromGivenState(state: Vector[Map[String, Double]]): State = {
    val realVectors = state.map(x => x.map { case (key, value) => (key, value)}).map(RealVector.fromMap)
    realVectors.map(v => (v, f(v))).minBy(_._2) |> RS_State.tupled
  }

  override def initialize(f: Function, area: OptimizationAlgorithm.Area,
                          state: Option[Vector[Map[String, Double]]]): Unit = {
    possibleDelta = area.map { case (key, value) =>
      val width: Double = value._2 - value._1
      (key, (-deltaRatio * width, deltaRatio * width))
    }
    super.initialize(f, area, state)
  }

  override def iterate(): Unit = {
    val RS_State(currentPoint, currentValue) = currentState

    currentState = (1 to numberOfAttempts)
      .foldLeft((currentPoint, currentValue)) { case ((v, value), _) =>
        val delta = GoRN.getContinuousUniform(possibleDelta) |> RealVector.apply
        val _v = (currentPoint + delta).constrain(area)
        val _value = f(_v)
        if (value < _value) (v, value)
        else (_v, _value)
      } |> RS_State.tupled
  }

}

object RandomSearch {

  case class RS_State(v: RealVector, value: Double) extends State {

    def apply(v: RealVector, value: Double): RS_State = RS_State(v, value)

    override def toVectors(): Vector[RealVector] = Vector(v)

    override def getBestBy(f: Function): RealVector = v

  }

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