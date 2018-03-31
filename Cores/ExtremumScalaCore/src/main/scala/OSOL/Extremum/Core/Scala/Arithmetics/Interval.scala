package OSOL.Extremum.Core.Scala.Arithmetics

import Interval.Exceptions._

/** Represents interval numbers in the form `[a; b]`
  *
  * @param lowerBound min value `a` of the interval
  * @param upperBound max value `b` of the interval
  *
  */
class Interval private (val lowerBound: Double, val upperBound: Double) {

  /** Gets middle point if the interval */
  final lazy val middlePoint: Double = 0.5 * (lowerBound + upperBound)
  /** Gets width of the interval */
  final lazy val width: Double = upperBound - lowerBound
  /** Gets radius of the interval */
  final lazy val radius: Double = width / 2.0

  /** Converts Interval to String
    *
    * @return string representation of Interval
    */
  final override def toString: String = s"[$lowerBound; $upperBound]"

  /** Deremines whether objects are equal or not
    *
    * @param that second object
    * @return equal or not
    */
  final def equalsTo(that: Interval): Boolean =
    this.lowerBound == that.lowerBound && this.upperBound == that.upperBound
  /** Same as [[OSOL.Extremum.Core.Scala.Arithmetics#equalsTo equalsTo]] */
  final def ==(that: Interval): Boolean = this.equalsTo(that)

  /** Deremines whether objects are approximately equal
    *
    * @param that second object
    * @param maxError maximum allowed difference
    * @return equal or not
    */
  final def approximatelyEqualsTo(that: Interval, maxError:Double): Boolean = {
    def getDifference(a: Double, b: Double): Double = {
      val delta = math.abs(a - b)
      if (delta.isNaN) {
        if (a == b) 0.0
        else 1.0
      }
      else delta
    }
    val errorLeft = getDifference(this.lowerBound, that.lowerBound)
    val errorRight = getDifference(this.upperBound, that.upperBound)
    errorLeft + errorRight <= maxError
  }
  /** Same as [[OSOL.Extremum.Core.Scala.Arithmetics#approximatelyEqualsTo approximatelyEqualsTo]] */
  final def ~(that: Interval, maxError: Double = 1e-5): Boolean = this.approximatelyEqualsTo(that, maxError)

  /** Negates current Interval `[a; b]`
    *
    * @return `[-b; -a]`
    */
  final def neg(): Interval =
    Interval(-upperBound, -lowerBound)
  /** Same as [[OSOL.Extremum.Core.Scala.Arithmetics#neg neg]] */
  final def unary_-(): Interval = this.neg()

  /** Calculates sum of two intervals
    *
    * @param that second term
    * @return sum of `this + that`
    */
  final def add(that: Interval): Interval =
    Interval(this.lowerBound + that.lowerBound, this.upperBound + that.upperBound)
  /** Same as [[OSOL.Extremum.Core.Scala.Arithmetics#add add]] */
  final def +(that: Interval): Interval = this.add(that)

  /** Calculates difference of two intervals
    *
    * @param that second term
    * @return sum of `this - that`
    */
  final def sub(that: Interval): Interval =
    Interval(this.lowerBound - that.upperBound, this.upperBound - that.lowerBound)
  /** Same as [[OSOL.Extremum.Core.Scala.Arithmetics#sub sub]] */
  final def -(that: Interval): Interval = this.sub(that)

  /** Calculates product of two intervals
    *
    * @param that second term
    * @return sum of `this * that`
    */
  final def mul(that: Interval): Interval = {
    val products = Seq(
      this.lowerBound * that.lowerBound,
      this.lowerBound * that.upperBound,
      this.upperBound * that.lowerBound,
      this.upperBound * that.upperBound)

    Interval(products.min, products.max)
  }
  /** Same as [[OSOL.Extremum.Core.Scala.Arithmetics#mul mul]] */
  final def *(that: Interval): Interval = this.mul(that)

  /** Calculates quotient of two intervals
    *
    * @param that second term
    * @return sum of `this / that`
    */
  final def div(that: Interval): Interval = {
    that match {
      case _ if that.lowerBound > 0.0 || that.upperBound < 0.0 => this.mul(Interval(1.0 / that.upperBound, 1.0 / that.lowerBound))
      case _ if that.lowerBound == 0.0 => this.mul(Interval(1.0 / that.upperBound, Double.PositiveInfinity))
      case _ if that.upperBound == 0.0 => this.mul(Interval(Double.NegativeInfinity, 1 / that.lowerBound))
      case _ => Interval(Double.NegativeInfinity, Double.PositiveInfinity)
    }
  }
  /** Same as [[OSOL.Extremum.Core.Scala.Arithmetics#div div]] */
  final def /(that: Interval): Interval = this.div(that)

  /** Calculates power of two intervals
    *
    * @param that second term
    * @return sum of `this \^ that`
    */
  final def pow(that: Interval): Interval = {
    if (that.width != 0) throw new UnknownOperationException("[a; b] ^ [c; d] for (d - c) > 0")
    else {
      val powerIndex: Int = that.middlePoint.toInt
      val values = Seq(math.pow(lowerBound, powerIndex), math.pow(upperBound, powerIndex)).sorted
      (that, values) match {
        case (_, a :: b :: _) if powerIndex % 2 == 0 => if (lowerBound * upperBound <= 0.0) Interval(0.0, b) else Interval(a, b)
        case (_, a :: b :: _) => Interval(a, b)
      }
    }
  }
  /** Same as [[OSOL.Extremum.Core.Scala.Arithmetics#pow pow]] */
  final def ^(that: Interval): Interval = this.pow(that)
  /** Same as [[OSOL.Extremum.Core.Scala.Arithmetics#pow pow]] */
  final def **(that: Interval): Interval = this.pow(that)

  /** Calculates `abs(this)`
    *
    * @return absolute value
    */
  final def abs(): Interval = {
    val values = Seq(math.abs(lowerBound), math.abs(upperBound)).sorted
    values match {
      case _ :: b :: _ if lowerBound * upperBound <= 0.0 => Interval(0.0, b)
      case a :: b :: _ => Interval(a, b)
    }
  }

  /** Calculates `sin(this)`
    *
    * @return sine value
    */
  final def sin(): Interval = {
    if (width > 2.0 * math.Pi) Interval(-1.0, 1.0)
    else {
      val c = 0.5 * math.Pi
      val leftBound = math.ceil(lowerBound / c).toInt
      val rightBound = math.floor(upperBound / c).toInt
      val points = lowerBound +: upperBound +: (leftBound to rightBound).map(c * _)
      val mappedPoints = points.map(math.sin).sorted
      Interval(mappedPoints.head, mappedPoints.last)
    }
  }

  /** Calculates `cos(this)`
    *
    * @return cosine value
    */
  final def cos(): Interval = {
    if (width > 2.0 * math.Pi) Interval(-1.0, 1.0)
    else {
      val c = 0.5 * math.Pi
      val leftBound = math.ceil(lowerBound / c).toInt
      val rightBound = math.floor(upperBound / c).toInt
      val points = lowerBound +: upperBound +: (leftBound to rightBound).map(c * _)
      val mappedPoints = points.map(math.cos).sorted
      Interval(mappedPoints.head, mappedPoints.last)
    }
  }

  /** Calculates `exp(this)`
    *
    * @return exponent value
    */
  final def exp(): Interval = Interval(math.exp(lowerBound), math.exp(upperBound))

  /** Calculates `sqrt(this)`
    *
    * @return square root value
    */
  final def sqrt(): Interval = {
    if (upperBound < 0.0) throw new BadAreaOperationException(opName = "sqrt", this)
    else {
      if (lowerBound < 0.0) Interval(0.0, math.sqrt(upperBound))
      else Interval(math.sqrt(lowerBound), math.sqrt(upperBound))
    }
  }

  /** Calculates `ln(this)`
    *
    * @return natural logarithm value
    */
  final def ln(): Interval = {
    if (upperBound < 0.0) throw new BadAreaOperationException(opName = "ln", this)
    else {
      if (lowerBound < 0.0) Interval(Double.NegativeInfinity, math.log(upperBound))
      else Interval(math.log(lowerBound), math.log(upperBound))
    }
  }

  /** Moves current interval according to `delta` value
    *
    * @param delta movement value
    * @return moved interval
    */
  final def moveBy(delta: Double): Interval = this.add(Interval(delta))

  /** Forces interval to be located in `[min; max]` interval
    *
    * @param min minimum allowed value
    * @param max maximum allowed value
    * @return constrained interval
    */
  final def constrain(min: Double, max: Double): Interval = {
    def check(value: Double) =
      if (value < min) min
      else {
        if (value > max) max
        else value
      }
    Interval(check(lowerBound), check(upperBound))
  }

}

/** Companion object for [[OSOL.Extremum.Core.Scala.Arithmetics.Interval Interval]] */
object Interval {

  import Converters._

  /** Minimal width to consider interval */
  var minWidth: Double = 1e-5

  /** Constructor that analyses width
    *
    * @param lowerBound min value of interval
    * @param upperBound max value of interval
    * @return degenerate interval (if `upperBound` - `lowerBound` < `minWidth`) or <p>
    *         ordinary interval ['lowerBound', 'upperBound']
    */
  final def apply(lowerBound: Double, upperBound: Double): Interval = {
    if (upperBound - lowerBound < minWidth) Interval(0.5 * (lowerBound + upperBound))
    else new Interval(lowerBound, upperBound)
  }

  /** Create Interval number from point
    *
    * @param value midpoint
    * @return degenerate interval [`value`; `value`]
    **/
  final def apply(value: Double): Interval = value

  /** Implicit converters for [[OSOL.Extremum.Core.Scala.Arithmetics.Interval Interval]] */
  object Converters {

    /** Converts Double value to Interval number
      *
      * @param value value to convert
      * */
    implicit def fromDouble(value: Double): Interval = new Interval(value, value)

    /** Converts String value to Interval number
      *
      * @param value value to convert
      * */
    implicit def fromString(value: String): Interval = {
      val split = value.drop(1).dropRight(1).split(";")
      if (split.length == 2) Interval(split(0).toDouble, split(1).toDouble)
      else fromDouble(value.toDouble)
    }

    /** Converts pair of values (a, b) to Interval number
      *
      * @param pair value to convert
      * @return interval [`pair_1`; `pair_2`]
      * */
    implicit def fromPair(pair: (Double, Double)): Interval = Interval(pair._1, pair._2)

  }

  /** Exceptions that can be raised for [[OSOL.Extremum.Core.Scala.Arithmetics.Interval Interval]] */
  object Exceptions {

    /** Exception for unsupported operation
      *
      * @param opName operation name
      */
    class UnknownOperationException(opName: String) extends Exception

    /** Exception for bad operation argument
      *
      * @param opName operation name
      * @param interval bad interval
      */
    class BadAreaOperationException(opName: String, interval: Interval) extends Exception

  }

}