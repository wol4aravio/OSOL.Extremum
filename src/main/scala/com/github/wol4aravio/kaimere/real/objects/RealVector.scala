package com.github.wol4aravio.kaimere.real.objects

import RealVector._
import RealVector.Exceptions._

case class RealVector(private val vals: Map[String, Double]) {

  def keys: Iterable[String] = vals.keys
  def keySet: Set[String] = vals.keySet

  def values: Iterable[Double] = vals.values

  def apply(key: String): Double = vals(key)

  def getOrElse(key: String, default: Double): Double = vals.getOrElse(key, default)

  def apply(key: String, default: Double): Double = this.getOrElse(key, default)

  def ==(that: RealVector): Boolean = {
    val (allKeys, same) = checkKeys(this, that)
    if (!same) throw new DifferentKeysException(Seq(this, that).map(_.keySet):_*)
    else allKeys.forall(key => this(key) == that(key))
  }

  def +(that: RealVector): RealVector = {
    val (allKeys, same) = checkKeys(this, that)
    if (!same) throw new DifferentKeysException(Seq(this, that).map(_.keySet):_*)
    else allKeys.map(key => (key, this(key) + that(key))).toMap[String, Double]
  }

  def ~+(that: RealVector): RealVector = {
    val (allKeys, _) = checkKeys(this, that)
    allKeys.map(key => (key, this(key, 0.0) + that(key, 0.0))).toMap[String, Double]
  }

  def moveBy(delta: Map[String, Double]): RealVector = this ~+ delta

  def *(coeff: Double): RealVector = vals.mapValues(coeff * _)

  def unary_-(): RealVector = this * (-1)

  def -(that: RealVector): RealVector = this + (-that)

  def ~-(that: RealVector): RealVector = this ~+ (-that)

  def constrain(area: Map[String, (Double, Double)]): RealVector = {
    this.keySet
      .map { key =>
        val currentValue = this (key)
        val (min, max) = area.getOrElse(key, (Double.NegativeInfinity, Double.PositiveInfinity))
        val constrainedValue =
          if (currentValue > max) max
          else {
            if (currentValue < min) min
            else currentValue
          }
        (key, constrainedValue)
      }.toMap[String, Double]
  }

}

object RealVector {

  object Exceptions {

    class DifferentKeysException(keys: Set[String]*) extends Exception

  }

  def apply(pairs: (String, Double)*): RealVector = RealVector(pairs.toMap[String, Double])

  implicit def fromMap(values: Map[String, Double]): RealVector = RealVector(values)

  def checkKeys(vectors: RealVector*): (Set[String], Boolean) = {
    val allKeys = vectors.map(_.keySet).reduce(_ ++ _)
    (allKeys, vectors.forall(_.keySet == allKeys))
  }

}
