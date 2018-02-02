package kaimere.real.optimization.general

import kaimere.real.objects.{Function, RealVector}
import kaimere.real.objects.RealVector._
import spray.json._

class State(vectors: Vector[RealVector]) {

  final def toVectors(): Vector[RealVector]  = vectors

  def getBestBy(f: Function): (RealVector, Double) = vectors.map(v => (v, f(v))).minBy(_._2)

}

object State {

  implicit def toVectorMap(s: State): Vector[Map[String, Double]] = s.toVectors().map(_.vals)

  implicit object StateJsonFormat extends RootJsonFormat[State] {
    def write(s: State) = JsObject("vectors" -> JsArray(s.toVectors().map(_.toJson)))

    def read(json: JsValue): State = {
      val Seq(vectorArray) = json.asJsObject.getFields("vectors")
      vectorArray match {
        case JsArray(array) =>
          val vectors = array.map(_.convertTo[RealVector])
          new State(vectors)
        case _ => throw DeserializationException("State Expected")
      }
    }
  }

}