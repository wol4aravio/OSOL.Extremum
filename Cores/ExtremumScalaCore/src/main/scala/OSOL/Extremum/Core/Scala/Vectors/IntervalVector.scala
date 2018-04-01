package OSOL.Extremum.Core.Scala.Vectors

import OSOL.Extremum.Core.Scala.Arithmetics.Interval
import IntervalVector.Converters._
import OSOL.Extremum.Core.Scala.CodeFeatures.Pipe

/** Interval valued vector
  *
  * @param values values which form VectorObject (key-value pairs)
  */
class IntervalVector private (override val values: Map[String, Interval]) extends VectorObject[Interval](values) {

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
    val constrainedVector = this.values.map { case (k, value) => (k,
      k match {
        case _ if restrictingArea.isDefinedAt(k) =>
          Interval(constrainValue(value.lowerBound, restrictingArea(k)), constrainValue(value.upperBound, restrictingArea(k)))
        case _ => value
      })
    }
    constrainedVector
  }
}

/** Companion object for [[OSOL.Extremum.Core.Scala.Vectors.IntervalVector IntervalVector]] class */
object IntervalVector {

  /** Implicit converters for [[OSOL.Extremum.Core.Scala.Vectors.IntervalVector IntervalVector]] */
  object Converters {

    /** Converts `Iterable[(String, Interval)]` to [[OSOL.Extremum.Core.Scala.Vectors.IntervalVector IntervalVector]]
      *
      * @param v `(key, value)` pairs
      * @return [[OSOL.Extremum.Core.Scala.Vectors.IntervalVector IntervalVector]]
      */
    implicit def Iterable_to_IntervalVector(v: Iterable[(String, Interval)]): IntervalVector = IntervalVector(v)

  }

  /** Create object from `(key, value)` pairs
    *
    * @param keyValuePairs target `(key, value)` pairs
    * @return vector composed of `keyValuePairs`
    */
  final def apply(keyValuePairs: (String, Interval)*): IntervalVector = new IntervalVector(keyValuePairs.toMap)
  /** Create object from `(key, value)` pairs
    *
    * @param keyValuePairs target `(key, value)` pairs
    * @return vector composed of `keyValuePairs`
    */
  final def apply(keyValuePairs: Iterable[(String, Interval)]): IntervalVector = IntervalVector(keyValuePairs.toSeq:_*)


}