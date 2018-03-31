package OSOL.Extremum.Core.Scala.Vectors

import RealVector.Converters._
import OSOL.Extremum.Core.Scala.CodeFeatures.Pipe

/** Ordinary numerical vector
  *
  * @param vals values which form VectorObject (key-value pairs)
  */
class RealVector private (override val vals: Map[String, Double]) extends VectorObject[Double](vals) {

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
    val constrainedVector = this.vals.map { case (k, value) => (k,
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
  final def apply(keyValuePairs: Iterable[(String, Double)]): RealVector = RealVector(keyValuePairs.toSeq:_*)


}