package kaimere.real.optimization.classic.zero_order

import kaimere.real.optimization._
import kaimere.real.optimization.general._
import kaimere.real.objects.{Function, RealVector}
import kaimere.real.optimization.general.initializers.Initializer
import kaimere.tools.random.GoRN
import kaimere.tools.etc._
import spray.json._

case class RatioFluctuationSearch(numberOfAttempts: Int, fluctuationRatio: Double) extends OptimizationAlgorithm {

  case class RS_State(v: RealVector, value: Double) extends State(vectors = Vector(v)) {

    override def getBestBy(f: Function): (RealVector, Double) = (v, value)

  }

  override def initializeFromGivenState(state: State): State = {
    val realVectors = Helper.prepareInitialState(state)
    val bestVector = Helper.chooseOneBest(realVectors, f)
    (bestVector, f(bestVector)) |> RS_State.tupled
  }

  private var possibleRatio: Map[String, (Double, Double)] = null

  override def initialize(f: Function, area: OptimizationAlgorithm.Area,
                          state: Option[State], initializer: Initializer): Unit = {
    possibleRatio = area.map { case (key, value) =>
      val width: Double = value._2 - value._1
      (key, (1.0 - fluctuationRatio, 1.0 + fluctuationRatio))
    }
    super.initialize(f, area, state, initializer)
  }

  override def iterate(): Unit = {
    val RS_State(currentPoint, currentValue) = currentState

    currentState = (1 to numberOfAttempts)
      .foldLeft((currentPoint, currentValue)) { case ((v, value), _) =>
        val ratio = GoRN.getContinuousUniform(possibleRatio) |> RealVector.apply
        val _v = (currentPoint * ratio).constrain(area)
        val _value = f(_v)
        if (value < _value) (v, value)
        else (_v, _value)
      } |> RS_State.tupled
  }

}

object RatioFluctuationSearch {

  def apply(csv: String): RatioFluctuationSearch = {
    val Array(name, numberOfAttempts, fluctuationRatio) = csv.split(",")
    name match {
      case "RFS" | "rfs" | "RatioFluctuationSearch" => RatioFluctuationSearch(numberOfAttempts.toInt, fluctuationRatio.toDouble)
      case _ => throw DeserializationException("RatioFluctuationSearch expected")
    }
  }

  implicit object RatioFluctuationSearchJsonFormat extends RootJsonFormat[RatioFluctuationSearch] {
    def write(rs: RatioFluctuationSearch) =
      JsObject(
        "name" -> JsString("RatioFluctuationSearch"),
        "numberOfAttempts" -> JsNumber(rs.numberOfAttempts),
        "fluctuationRatio" -> JsNumber(rs.fluctuationRatio))

    def read(json: JsValue): RatioFluctuationSearch =
      json.asJsObject.getFields("name", "numberOfAttempts", "fluctuationRatio") match {
        case Seq(JsString(name), JsNumber(numberOfAttempts), JsNumber(fluctuationRatio)) =>
          if (name != "RatioFluctuationSearch") throw DeserializationException("RatioFluctuationSearch expected")
          else RatioFluctuationSearch(Seq(name, numberOfAttempts, fluctuationRatio).mkString(","))
        case _ => throw DeserializationException("RatioFluctuationSearch expected")
      }
  }

}