package OSOL.Extremum.Core.Scala.Vectors

import RealVector.Converters._
import OSOL.Extremum.Core.Scala.CodeFeatures.Pipe
import OSOL.Extremum.Core.Scala.Optimization.Optimizable
import OSOL.Extremum.Core.Scala.Vectors.Exceptions.DifferentKeysException
import spray.json._

/** Ordinary numerical vector
  *
  * @param elements values which form VectorObject (key-value pairs)
  */
class RealVector private (override val elements: Map[String, Double])
  extends VectorObject[Double](elements) with Optimizable[RealVector, Double] {

  final override def equalsTo(that: VectorObject[Double]): Boolean = {
    val keys_1 = this.keys
    val keys_2 = that.keys
    if (keys_1 != keys_2) throw new DifferentKeysException(keys_1, keys_2)
    else keys_1.forall(k => this(k) == that(k))
  }

  final override def add(that: VectorObject[Double]): RealVector =
    this.elementWiseOp(that, (a, b) => a + b)

  final override def addImputeMissingKeys(that: VectorObject[Double]): RealVector =
    this.elementWiseOpImputeMissingKeys(that, (a, b) => a + b, 0.0)

  final override def multiply(that: VectorObject[Double]): RealVector =
    this.elementWiseOp(that, (a, b) => a * b)

  final override def multiplyImputeMissingKeys(that: VectorObject[Double]): RealVector =
    this.elementWiseOpImputeMissingKeys(that, (a, b) => a * b, 1.0)

  final override def multiply(coefficient: Double): RealVector =
    this.keys.map(k => (k, coefficient * this (k))) |> RealVector.apply

  final override def moveBy(delta: (String, Double)*): RealVector = {
    val deltaWithImputedValues = delta ++ this.keys.diff(delta.map(_._1).toSet).map(k => (k, 0.0))
    this.add(deltaWithImputedValues |> RealVector.apply)
  }

  final override def constrain(area: (String, (Double, Double))*): RealVector = {
    val restrictingArea = area.toMap
    val constrainedVector = this.elements.map { case (k, value) => (k,
      k match {
        case _ if restrictingArea.isDefinedAt(k) =>
          val (min, max) = restrictingArea(k)
          if (value > max) max
          else {
            if (value < min) min
            else value
          }
        case _ => value
      })
    }
    constrainedVector
  }

  final override def getPerformance(f: Map[String, Double] => Double): Double = f(this.elements)

  final override def toBasicForm(): VectorObject[Double] = this

  import RealVector.RealVectorJsonFormat._
  final override def convertToJson(): JsValue = this.toJson

}

/** Companion object for [[OSOL.Extremum.Core.Scala.Vectors.RealVector RealVector]] class */
object RealVector {

  /** Implicit converters for [[OSOL.Extremum.Core.Scala.Vectors.RealVector RealVector]] */
  object Converters {

    /** Converts `Iterable[(String, Double)]` to [[OSOL.Extremum.Core.Scala.Vectors.RealVector RealVector]]
      *
      * @param v `(key, value)` pairs
      * @return [[OSOL.Extremum.Core.Scala.Vectors.RealVector RealVector]]
      */
    implicit def Iterable_to_RealVector(v: Iterable[(String, Double)]): RealVector = RealVector(v)

    /** Converts `VectorObject[Double]` to [[OSOL.Extremum.Core.Scala.Vectors.RealVector RealVector]]
      *
      * @param v `VectorObject[Double]`
      * @return [[OSOL.Extremum.Core.Scala.Vectors.RealVector RealVector]]
      */
    implicit def VectorObject_to_RealVector(v: VectorObject[Double]): RealVector = RealVector(v.elements)

  }

  /** Create object from `(key, value)` pairs
    *
    * @param keyValuePairs target `(key, value)` pairs
    * @return vector composed of `keyValuePairs`
    */
  final def apply(keyValuePairs: (String, Double)*): RealVector = new RealVector(keyValuePairs.toMap)

  /** Create object from `(key, value)` pairs
    *
    * @param keyValuePairs target `(key, value)` pairs
    * @return vector composed of `keyValuePairs`
    */
  final def apply(keyValuePairs: Iterable[(String, Double)]): RealVector = RealVector(keyValuePairs.toSeq: _*)

  /** Json Serialization for RealVector */
  implicit object RealVectorJsonFormat extends RootJsonFormat[RealVector] {
    def write(v: RealVector) = JsObject(
      "RealVector" -> JsObject(
        "elements" -> JsArray(
          v.elements.map { case (k, v) =>
            JsObject("key" -> JsString(k), "value" -> JsNumber(v))
          }.toVector)))

    def read(json: JsValue): RealVector =
      json.asJsObject.getFields("RealVector") match {
        case Seq(realVector) => realVector.asJsObject.getFields("elements") match {
          case Seq(JsArray(elements)) => {
            val keyValuePairs = elements.map { e =>
              e.asJsObject.getFields("key", "value") match {
                case Seq(JsString(k), JsNumber(v)) => k -> v.toDouble
                case _ => throw DeserializationException("No necessary fields")
              }
            }
            keyValuePairs.toMap
          }
          case _ => throw DeserializationException("No necessary fields")
        }
        case _ => throw DeserializationException("No RealVector Field")
      }
  }

}