package OSOL.Extremum.Core.Scala.Vectors

import OSOL.Extremum.Core.Scala.Arithmetics.Interval
import IntervalVector.Converters._
import OSOL.Extremum.Core.Scala.CodeFeatures.Pipe
import OSOL.Extremum.Core.Scala.Optimization.Optimizable
import OSOL.Extremum.Core.Scala.Vectors.Exceptions.DifferentKeysException

/** Interval valued vector
  *
  * @param values values which form VectorObject (key-value pairs)
  */
class IntervalVector private (override val values: Map[String, Interval])
  extends VectorObject[Interval](values) with Optimizable[IntervalVector, Interval] {

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
    val constrainedVector = this.values.map { case (k, value) => (k,
      k match {
        case _ if restrictingArea.isDefinedAt(k) =>
          Interval(constrainValue(value.lowerBound, restrictingArea(k)), constrainValue(value.upperBound, restrictingArea(k)))
        case _ => value
      })
    }
    constrainedVector
  }

  final override def getPerformance(f: Map[String, Interval] => Interval): Double = f(this.values).lowerBound

  final override def toBasicForm(): VectorObject[Double] = RealVector(this.values.mapValues(_.middlePoint))

  final def split(ratios: Seq[Double], key: Option[String] = None): Seq[IntervalVector] = {
    val splitKey =
      if (key.isDefined) key.get
      else values.minBy { case (k, v) => -v.width }._1

    val splitComponent = this(splitKey).split(ratios)
    splitComponent.map { i => IntervalVector(this.values + (splitKey -> i))}
  }

  final def bisect(key: Option[String] = None): (IntervalVector, IntervalVector) = {
    val Seq(left, right) = this.split(Seq(1.0, 1.0), key)
    (left, right)
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

    /** Converts `VectorObject[Double]` to [[OSOL.Extremum.Core.Scala.Vectors.IntervalVector IntervalVector]]
      *
      * @param v `VectorObject[Double]`
      * @return [[OSOL.Extremum.Core.Scala.Vectors.IntervalVector IntervalVector]]
      */
    implicit def VectorObject_to_IntervalVector(v: VectorObject[Interval]): IntervalVector = IntervalVector(v.values)

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