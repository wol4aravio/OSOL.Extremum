package kaimere.real.optimization.metaheuristic

import kaimere.real.optimization.general._
import kaimere.real.objects.{Function, RealVector}
import kaimere.real.optimization._
import kaimere.real.optimization.metaheuristic.SimulatedAnnealing.SA_State
import kaimere.tools.random.GoRN
import kaimere.tools.etc._
import spray.json._

case class SimulatedAnnealing(alpha: Double, beta: Double = 1.0, gamma: Double = 1.0, initialTemp: Double) extends OptimizationAlgorithm {

  override def initializeFromGivenState(state: Vector[Map[String, Double]]): State = {
    val realVectors = Helper.prepareInitialState(state)
    val bestVector = Helper.chooseOneBest(realVectors, f)
    (bestVector, f(bestVector), 0) |> SA_State.tupled
  }

  override def iterate(): Unit = {

    val SA_State(v, value, id) = currentState

    val temp = initialTemp * math.pow(alpha, id)
    val deltas = area.map { case (name, _) => (name, GoRN.getNormal(0.0, math.sqrt(temp))) }

    val _v = v.moveBy(deltas).constrain(area)
    val _value = f(_v)

    val deltaValues = _value - value
    currentState = {
      if (deltaValues < 0.0) (_v, _value, id + 1)
      else {
        val acceptProbability = math.exp(-gamma * deltaValues / (beta * temp))
        if (GoRN.getContinuousUniform(0.0, 1.0) <= acceptProbability) (_v, _value, id + 1)
        else (v, value, id + 1)
      }
    } |> SA_State.tupled
  }
}

object SimulatedAnnealing {

  def apply(csv: String): SimulatedAnnealing = {
    val Array(name, alpha, beta, gamma, initialTemp) = csv.split(",")
    name match {
      case "SA" | "sa" | "SimulatedAnnealing" => SimulatedAnnealing(alpha.toDouble, beta.toDouble, gamma.toDouble, initialTemp.toDouble)
      case _ => throw DeserializationException("SimulatedAnnealing expected")
    }
  }

  case class SA_State(v: RealVector, value: Double, id: Int) extends State(vectors = Vector(v)) {

    override def getBestBy(f: Function): (RealVector, Double) = (v, value)

  }

  def apply(v_value_id: (RealVector, Double, Int)): SA_State = new SA_State(v_value_id._1, v_value_id._2, v_value_id._3)

  implicit object SimulatedAnnealingJsonFormat extends RootJsonFormat[SimulatedAnnealing] {
    def write(sa: SimulatedAnnealing) =
      JsObject(
        "name" -> JsString("SimulatedAnnealing"),
        "alpha" -> JsNumber(sa.alpha),
        "beta" -> JsNumber(sa.beta),
        "gamma" -> JsNumber(sa.gamma),
        "initialTemp" -> JsNumber(sa.initialTemp))

    def read(json: JsValue): SimulatedAnnealing =
      json.asJsObject.getFields("name", "alpha", "beta", "gamma", "initialTemp") match {
        case Seq(JsString(name), JsNumber(alpha), JsNumber(beta), JsNumber(gamma), JsNumber(initialTemp)) =>
          if (name != "SimulatedAnnealing") throw DeserializationException("SimulatedAnnealing expected")
          else SimulatedAnnealing(Seq(name, alpha, beta, gamma, initialTemp).mkString(","))
        case _ => throw DeserializationException("SimulatedAnnealing expected")
      }
  }

}