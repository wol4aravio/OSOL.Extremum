package OSOL.Extremum.Cores.JVM.Vectors

import RealVector.Converters._
import OSOL.Extremum.Cores.JVM.Pipe
import OSOL.Extremum.Cores.JVM.Vectors.Exceptions.DifferentKeysException
import OSOL.Extremum.Cores.JVM.Optimization.Optimizable
import spray.json._

class RealVector private (override val elements: Map[String, java.lang.Double])
  extends VectorObject[java.lang.Double](elements) with Optimizable[RealVector, java.lang.Double] {

  final override def equalsTo(that: VectorObject[java.lang.Double]): java.lang.Boolean = {
    val keys_1 = this.keys
    val keys_2 = that.keys
    if (keys_1 != keys_2) throw new DifferentKeysException(keys_1, keys_2)
    else keys_1.forall(k => this(k) == that(k))
  }

  final override def add(that: VectorObject[java.lang.Double]): RealVector =
    this.elementWiseOp(that, (a, b) => a + b)

  final override def addImputeMissingKeys(that: VectorObject[java.lang.Double]): RealVector =
    this.elementWiseOpImputeMissingKeys(that, (a, b) => a + b, 0.0)

  final override def multiply(that: VectorObject[java.lang.Double]): RealVector =
    this.elementWiseOp(that, (a, b) => a * b)

  final override def multiplyImputeMissingKeys(that: VectorObject[java.lang.Double]): RealVector =
    this.elementWiseOpImputeMissingKeys(that, (a, b) => a * b, 1.0)

  final override def multiply(coefficient: java.lang.Double): RealVector =
    this.keys.map(k => (k, coefficient * this (k)))

  final override def moveBy(delta: (String, java.lang.Double)*): RealVector = {
    val deltaWithImputedValues = delta ++ this.keys.diff(delta.map(_._1).toSet).map(k => (k, new java.lang.Double(0.0)))
    this.add(deltaWithImputedValues)
  }

  final override def constrain(area: (String, (java.lang.Double, java.lang.Double))*): RealVector = {
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

  final override def getPerformance(f: Map[String, java.lang.Double] => java.lang.Double): java.lang.Double = f(this.elements)

  final override def toBasicForm(): VectorObject[java.lang.Double] = this

  final override def union(that: (String, java.lang.Double)): VectorObject[java.lang.Double] = {
    val keys = this.keys + that._1
    keys.map(k => (k, if (that._1.equals(k)) that._2 else this (k)))
  }

  import RealVector.RealVectorJsonFormat._
  final override def convertToJson(): JsValue = this.toJson

  final override def distanceFromArea(area: Map[String, (java.lang.Double, java.lang.Double)]): Map[String, java.lang.Double] = {
    area.keySet.map { k =>
      val (min, max) = area(k)
      val v = this(k)
      (k, if (v < min) min - v
      else {
        if (v > max) v - max
        else 0.0
      })
    }.toMap.mapValues(new java.lang.Double(_))
  }

}

object RealVector {

  object Converters {

    implicit def IterableToRealVector(v: Iterable[(String, java.lang.Double)]): RealVector = RealVector(v)
    implicit def ScalaIterableToRealVector(v: Iterable[(String, Double)]): RealVector =
      RealVector(v.map { case (k, v) => (k, new java.lang.Double(v))})

    implicit def VectorObjectToRealVector(v: VectorObject[java.lang.Double]): RealVector = RealVector(v.elements)
    implicit def ScalaVectorObjectToRealVector(v: VectorObject[Double]): RealVector = v.elements

  }

  final def apply(keyValuePairs: (String, java.lang.Double)*): RealVector = new RealVector(keyValuePairs.toMap)

  final def apply(keyValuePairs: Iterable[(String, java.lang.Double)]): RealVector = RealVector(keyValuePairs.toSeq: _*)

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
            keyValuePairs.toMap.mapValues(new java.lang.Double(_))
          }
          case _ => throw DeserializationException("No necessary fields")
        }
        case _ => throw DeserializationException("No RealVector Field")
      }
  }

}