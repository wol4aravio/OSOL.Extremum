package kaimere.real.optimization.metaheuristic

import kaimere.real.optimization.general._
import kaimere.real.objects.{Function, RealVector}
import kaimere.real.optimization.metaheuristic.SimulatedAnnealing.SA_State
import kaimere.tools.random.GoRN
import kaimere.tools.etc._
import spray.json._

case class SimulatedAnnealing(alpha: Double, beta: Double = 1.0, gamma: Double = 1.0, initialTemp: Double) extends OptimizationAlgorithm {

  override def initializeRandomState(): State = {
    val v = GoRN.getContinuousUniform(area)
    val value = f(v)
    SA_State(v, value, 0)
  }

  override def initializeFromGivenState(state: Vector[Map[String, Double]]): State = {
    val realVectors = state.map(x => x.map { case (key, value) => (key, value) }).map(RealVector.fromMap)
    realVectors.map(v => (v, f(v), 0)).minBy(_._2) |> SA_State.tupled
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

  case class SA_State(v: RealVector, value: Double, id: Int) extends State {

    def apply(v: RealVector, value: Double, id: Int): SA_State = SA_State(v, value, id)

    override def toVectors(): Vector[RealVector] = Vector(v)

    override def getBestBy(f: Function): RealVector = v

  }

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
          else SimulatedAnnealing(alpha.toDouble, beta.toDouble, gamma.toDouble, initialTemp.toDouble)
        case _ => throw DeserializationException("SimulatedAnnealing expected")
      }
  }

}