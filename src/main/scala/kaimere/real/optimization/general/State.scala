package kaimere.real.optimization.general

import kaimere.real.objects.{RealVector, Function}
import kaimere.real.objects.RealVector._

import spray.json._

case class State(components: Vector[RealVector]) extends Traversable[RealVector] {

  final override def foreach[U](f: RealVector => U): Unit = components.foreach(f)

  final def apply(id: Int): RealVector = components(id)

  final def getBestBy(f: Function): RealVector = this.minBy(x => f(x))

}

object State {

  implicit object StateJsonFormat extends RootJsonFormat[State] {
    def write(s: State) =
      JsObject("components" -> JsArray(s.components.map(v => v.toJson)))

    def read(json: JsValue): State =
      json.asJsObject.getFields("components") match {
        case Seq(JsArray(jsonComponents)) =>
          val components = jsonComponents
            .map {
              case v => v.convertTo[RealVector]
              case _ => throw DeserializationException("RealVector expected")
            }
          State(components)
        case _ => throw DeserializationException("State expected")
      }
  }

}