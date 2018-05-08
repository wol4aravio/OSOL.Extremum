package OSOL.Extremum.Cores.JVM.Vectors

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import IntervalVector.Converters._
import OSOL.Extremum.Cores.JVM.Pipe
import OSOL.Extremum.Cores.JVM.Optimization.Optimizable
import OSOL.Extremum.Cores.JVM.Vectors.Exceptions.DifferentKeysException
import OSOL.Extremum.Cores.JVM.Optimization.Optimizable
import spray.json._

class IntervalVector private (override val elements: Map[String, Interval])
  extends VectorObject[Interval](elements) with Optimizable[IntervalVector, Interval] {

  final def equalsTo(that: VectorObject[Interval]): Boolean = {
    val keys_1 = this.keys
    val keys_2 = that.keys
    if (keys_1 != keys_2) throw new DifferentKeysException(keys_1, keys_2)
    else keys_1.forall(k => this(k) == that(k))
  }

  final override def add(that: VectorObject[Interval]): IntervalVector =
    this.elementWiseOp(that, (a, b) => a + b)

  final override def addImputeMissingKeys(that: VectorObject[Interval]): IntervalVector =
    this.elementWiseOpImputeMissingKeys(that, (a, b) => a + b, Interval(0.0))

  final override def multiply(that: VectorObject[Interval]): IntervalVector =
    this.elementWiseOp(that, (a, b) => a * b)

  final override def multiplyImputeMissingKeys(that: VectorObject[Interval]): IntervalVector =
    this.elementWiseOpImputeMissingKeys(that, (a, b) => a * b, Interval(1.0))

  final override def multiply(coefficient: Double): IntervalVector =
    this.keys.map(k => (k, Interval(coefficient, coefficient) * this (k))) |> IntervalVector.apply

  final override def moveBy(delta: (String, Double)*): IntervalVector = {
    val deltaWithImputedValues = (delta ++ this.keys.diff(delta.map(_._1).toSet).map(k => (k, 0.0)))
      .map { case (k, v) => (k, Interval(v))}
    this.add(deltaWithImputedValues |> IntervalVector.apply)
  }

  final override def constrain(area: (String, (Double, Double))*): IntervalVector = {
    def constrainValue(value: Double, restrictingArea: (Double, Double)): Double = {
      val (min, max) = restrictingArea
      if (value > max) max
      else {
        if (value < min) min
        else value
      }
    }
    val restrictingArea = area.toMap
    val constrainedVector = this.elements.map { case (k, value) => (k,
      k match {
        case _ if restrictingArea.isDefinedAt(k) =>
          Interval(constrainValue(value.lowerBound, restrictingArea(k)), constrainValue(value.upperBound, restrictingArea(k)))
        case _ => value
      })
    }
    constrainedVector
  }

  final override def getPerformance(f: Map[String, Interval] => Interval): Double = f(this.elements).lowerBound

  final override def toBasicForm(): VectorObject[Double] = RealVector(this.elements.mapValues(_.middlePoint))

  final def split(ratios: Seq[Double], key: Option[String] = None): Seq[IntervalVector] = {
    val splitKey =
      if (key.isDefined) key.get
      else elements.minBy { case (k, v) => -v.width }._1

    val splitComponent = this(splitKey).split(ratios)
    splitComponent.map { i => IntervalVector(this.elements + (splitKey -> i))}
  }

  final def bisect(key: Option[String] = None): (IntervalVector, IntervalVector) = {
    val Seq(left, right) = this.split(Seq(1.0, 1.0), key)
    (left, right)
  }

  final override def union(that: (String, Interval)): VectorObject[Interval] = {
    val keys = this.keys + that._1
    keys.map(k => (k, if (that._1.equals(k)) that._2 else this (k)))
  }

  import IntervalVector.IntervalVectorJsonFormat._
  final override def convertToJson(): JsValue = this.toJson

  final override def distanceFromArea(area: Map[String, (Double, Double)]): Map[String, Double] = {
    area.keySet.map { k =>
      val (min, max) = area(k)
      def distance(v: Double): Double = {
        if (v < min) min - v
        else {
          if (v > max) v - max
          else 0.0
        }
      }
      (k, math.max(distance(this(k).lowerBound), distance(this(k).upperBound)))
    }.toMap
  }

}

object IntervalVector {

  object Converters {

    implicit def Iterable_to_IntervalVector(v: Iterable[(String, Interval)]): IntervalVector = IntervalVector(v)

    implicit def VectorObject_to_IntervalVector(v: VectorObject[Interval]): IntervalVector = IntervalVector(v.elements)

  }

  final def apply(keyValuePairs: (String, Interval)*): IntervalVector = new IntervalVector(keyValuePairs.toMap)
  final def apply(keyValuePairs: Iterable[(String, Interval)]): IntervalVector = IntervalVector(keyValuePairs.toSeq:_*)

  implicit object IntervalVectorJsonFormat extends RootJsonFormat[IntervalVector] {
    def write(v: IntervalVector) = JsObject(
      "IntervalVector" -> JsObject(
        "elements" -> JsArray(
          v.elements.map { case (k, v) =>
            JsObject("key" -> JsString(k), "value" -> v.toJson)
          }.toVector)))

    def read(json: JsValue): IntervalVector =
      json.asJsObject.getFields("IntervalVector") match {
        case Seq(intervalVector) => intervalVector.asJsObject.getFields("elements") match {
          case Seq(JsArray(elements)) => {
            val keyValuePairs = elements.map { e =>
              e.asJsObject.getFields("key", "value") match {
                case Seq(JsString(k), v) => k -> v.convertTo[Interval]
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