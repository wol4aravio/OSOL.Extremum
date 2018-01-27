package kaimere.real.optimization.general

import kaimere.real.objects.{RealVector, Function}
import kaimere.real.objects.RealVector._

import spray.json._

trait State {

  def toVectors(): Vector[RealVector]

  def getBestBy(f: Function): RealVector

}

object State {

  implicit object StateJsonFormat extends RootJsonFormat[State] {
    def write(s: State) =
      JsObject("components" -> JsArray(s.toVectors().map(v => v.toJson)))

    def read(json: JsValue): State = ???
  }

}