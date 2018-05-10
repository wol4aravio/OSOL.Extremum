package OSOL.Extremum.Cores.JVM.Vectors

import Exceptions._

abstract class VectorObject[Base] (val elements: Map[String, Base]) {

  final def keys: Set[String] = elements.keySet

  final def apply(key: String): Base = {
    try elements(key)
    catch {
      case _: Exception => throw new MissingKeyException(key)
    }
  }

  final def getOrElse(key: String, default: Base): Base = elements.getOrElse(key, default)
  final def apply(key: String, default: Base): Base = this.getOrElse(key, default)

  override def toString: String = elements.map { case (key, value) => s"$key -> $value" }.mkString("\n")

  final def elementWiseOp(that: VectorObject[Base], op: (Base, Base) => Base): Iterable[(String, Base)] = {
    val keys_1 = this.keys
    val keys_2 = that.keys
    if (keys_1 != keys_2) throw new DifferentKeysException(keys_1, keys_2)
    else keys_1.map(k => (k, op(this(k), that(k))))
  }

  final def elementWiseOpImputeMissingKeys(that: VectorObject[Base], op: (Base, Base) => Base, default: Base): Iterable[(String, Base)] = {
    val mergedKeys = this.keys.union(that.keys)
    mergedKeys.map(k => (k, op(this(k, default), that(k, default))))
  }

  def equalsTo(that: VectorObject[Base]): Boolean
  final def ==(that: VectorObject[Base]): Boolean = this.equalsTo(that)

  def add(that: VectorObject[Base]): VectorObject[Base]
  final def +(that: VectorObject[Base]): VectorObject[Base] = this.add(that)

  def addImputeMissingKeys(that: VectorObject[Base]): VectorObject[Base]
  final def ~+(that: VectorObject[Base]): VectorObject[Base] = this.addImputeMissingKeys(that)

  def multiply(coefficient: Double): VectorObject[Base]
  final def *(coefficient: Double): VectorObject[Base] = this.multiply(coefficient)

  final def neg(): VectorObject[Base] = this.multiply(-1)
  final def unary_-(): VectorObject[Base] = this.neg()

  final def subtract(that: VectorObject[Base]): VectorObject[Base] = this.add(that.multiply(-1))
  final def -(that: VectorObject[Base]): VectorObject[Base] = this.subtract(that)

  final def subtractImputeMissingKeys(that: VectorObject[Base]): VectorObject[Base] = this.addImputeMissingKeys(that.neg())
  final def ~-(that: VectorObject[Base]): VectorObject[Base] = this.subtractImputeMissingKeys(that)

  def multiply(that: VectorObject[Base]): VectorObject[Base]
  final def *(that: VectorObject[Base]): VectorObject[Base] = this.multiply(that)

  def multiplyImputeMissingKeys(that: VectorObject[Base]): VectorObject[Base]
  final def ~*(that: VectorObject[Base]): VectorObject[Base] = this.multiplyImputeMissingKeys(that)

  def union(that: (String, Base)): VectorObject[Base]
  def union(vectors: (String, Base)*): VectorObject[Base] = vectors.foldLeft(this) { case (a, b) => a.union(b) }

  def distanceFromArea(area: Map[String, (Double, Double)]): Map[String, Double]

}