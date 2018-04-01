package OSOL.Extremum.Core.Scala.Vectors

import Exceptions._

/** Current class is used as a base for vector objects
  *
  * @param values values which form VectorObject (key-value pairs)
  * @tparam Base value type
  */
abstract class VectorObject[Base] (val values: Map[String, Base]) {

  /** Returns all keys that are stored by current VectorObject
    *
    * @return keys
    */
  final def keys: Set[String] = values.keySet

  /** Access value by key
    *
    * @param key key to access
    * @return value that corresponds to 'key'
    */
  final def apply(key: String): Base = {
    try values(key)
    catch {
      case _: Exception => throw new MissingKeyException(key)
    }
  }

  /** Access value by its key with default
    *
    * @param key key to access
    * @param default value to return if key does not exist
    * @return value that corresponds to 'key' (if it exists), 'default' - otherwise
    */
  final def getOrElse(key: String, default: Base): Base = values.getOrElse(key, default)
  /** Same as [[OSOL.Extremum.Core.Scala.Vectors.VectorObject#getOrElse getOrElse]] */
  final def apply(key: String, default: Base): Base = this.getOrElse(key, default)

  /** Converts VectorObject to String
    *
    * @return string representation of VectorObject
    */
  override def toString: String = values.map { case (key, value) => s"$key -> $value" }.mkString("\n")

  /** Performs element-wise operation for pair of objects
    *
    * @param that second object
    * @param op operation to be performed
    * @return result of `op` application
    */
  final def elementWiseOp(that: VectorObject[Base], op: (Base, Base) => Base): Iterable[(String, Base)] = {
    val keys_1 = this.keys
    val keys_2 = that.keys
    if (keys_1 != keys_2) throw new DifferentKeysException(keys_1, keys_2)
    else keys_1.map(k => (k, op(this(k), that(k))))
  }

  /** Performs element-wise operation for pair of objects with imputation of missing values
    *
    * @param that second object
    * @param op operation to be performed
    * @param default imputation value
    * @return result of `op` application
    */
  final def elementWiseOpImputeMissingKeys(that: VectorObject[Base], op: (Base, Base) => Base, default: Base): Iterable[(String, Base)] = {
    val mergedKeys = this.keys.union(that.keys)
    mergedKeys.map(k => (k, op(this(k, default), that(k, default))))
  }

  /** Deremines whether objects are equal or not
    *
    * @param that second object
    * @return equal or not
    */
  def equalsTo(that: VectorObject[Base]): Boolean
  /** Same as [[OSOL.Extremum.Core.Scala.Vectors.VectorObject#equalsTo equalsTo]] */
  final def ==(that: VectorObject[Base]): Boolean = this.equalsTo(that)

  /** Adds another VectorObject to the current one
    *
    * @param that VectorObject to add
    * @return sum of VectorObjects
    */
  def add(that: VectorObject[Base]): VectorObject[Base]
  /** Same as [[OSOL.Extremum.Core.Scala.Vectors.VectorObject#add add]] */
  final def +(that: VectorObject[Base]): VectorObject[Base] = this.add(that)

  /** Adds another VectorObject to the current one with imputation of missing key-value pairs
    *
    * @param that VectorObject to add
    * @return sum of VectorObjects
    */
  def addImputeMissingKeys(that: VectorObject[Base]): VectorObject[Base]
  /** Same as [[OSOL.Extremum.Core.Scala.Vectors.VectorObject#addImputeMissingKeys addImputeMissingKeys]] */
  final def ~+(that: VectorObject[Base]): VectorObject[Base] = this.addImputeMissingKeys(that)

  /** Multiplies VectorObject by coefficient
    *
    * @param coefficient target coefficient
    * @return VectorObject scaled by 'coefficient'
    */
  def multiply(coefficient: Double): VectorObject[Base]
  /** Same as [[OSOL.Extremum.Core.Scala.Vectors.VectorObject#multiply multiply]] */
  final def *(coefficient: Double): VectorObject[Base] = this.multiply(coefficient)

  /** Negates current VectorObject
    *
    * @return VectorObject multiplied by (-1)
    */
  final def neg(): VectorObject[Base] = this.multiply(-1)
  /** Same as [[OSOL.Extremum.Core.Scala.Vectors.VectorObject#neg neg]] */
  final def unary_-(): VectorObject[Base] = this.neg()

  /** Subtracts another VectorObject from the current one
    *
    * @param that VectorObject to subtract
    * @return difference of VectorObjects
    */
  final def subtract(that: VectorObject[Base]): VectorObject[Base] = this.add(that.multiply(-1))
  /** Same as [[OSOL.Extremum.Core.Scala.Vectors.VectorObject#subtract subtract]] */
  final def -(that: VectorObject[Base]): VectorObject[Base] = this.subtract(that)

  /** Subtracts another VectorObject from the current one with imputation of missing key-value pairs
    *
    * @param that VectorObject to subtract
    * @return difference of VectorObjects
    */
  final def subtractImputeMissingKeys(that: VectorObject[Base]): VectorObject[Base] = this.addImputeMissingKeys(that.multiply(-1))
  /** Same as [[OSOL.Extremum.Core.Scala.Vectors.VectorObject#subtractImputeMissingKeys subtractImputeMissingKeys]] */
  final def ~-(that: VectorObject[Base]): VectorObject[Base] = this.subtractImputeMissingKeys(that)

  /** Multiplies current VectorObject by another one
    *
    * @param that VectorObject to multiply by
    * @return product of VectorObjects
    */
  def multiply(that: VectorObject[Base]): VectorObject[Base]
  /** Same as [[OSOL.Extremum.Core.Scala.Vectors.VectorObject#multiply multiply]] */
  final def *(that: VectorObject[Base]): VectorObject[Base] = this.multiply(that)

  /** Multiplies current VectorObject by another one with imputation of missing key-value pairs
    *
    * @param that VectorObject to multiply by
    * @return product of VectorObjects
    */
  def multiplyImputeMissingKeys(that: VectorObject[Base]): VectorObject[Base]
  /** Same as [[OSOL.Extremum.Core.Scala.Vectors.VectorObject#multiplyImputeMissingKeys multiplyImputeMissingKeys]] */
  final def ~*(that: VectorObject[Base]): VectorObject[Base] = this.multiplyImputeMissingKeys(that)

}