package OSOL.Extremum.Cores.JVM.Arithmetics

import Interval.Exceptions._
import spray.json._

class Interval private (val lowerBound: java.lang.Double, val upperBound: java.lang.Double) {

  final lazy val middlePoint: java.lang.Double = 0.5 * (lowerBound + upperBound)
  final lazy val width: java.lang.Double = upperBound - lowerBound
  final lazy val radius: java.lang.Double = width / 2.0

  final override def toString: String = s"[$lowerBound; $upperBound]"

  final def equalsTo(that: Interval): java.lang.Boolean =
    this.lowerBound == that.lowerBound && this.upperBound == that.upperBound

  final def ==(that: Interval): java.lang.Boolean = this.equalsTo(that)

  final def approximatelyEqualsTo(that: Interval, maxError:java.lang.Double): java.lang.Boolean = {
    def getDifference(a: java.lang.Double, b: java.lang.Double): java.lang.Double = {
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

  final def ~(that: Interval, maxError: java.lang.Double = 1e-5): java.lang.Boolean = this.approximatelyEqualsTo(that, maxError)

  final def neg(): Interval =
    Interval(-upperBound, -lowerBound)
  final def unary_-(): Interval = this.neg()

  final def add(that: Interval): Interval =
    Interval(this.lowerBound + that.lowerBound, this.upperBound + that.upperBound)
  final def +(that: Interval): Interval = this.add(that)

  final def sub(that: Interval): Interval =
    Interval(this.lowerBound - that.upperBound, this.upperBound - that.lowerBound)
  final def -(that: Interval): Interval = this.sub(that)

  final def mul(that: Interval): Interval = {
    val products = Seq(
      this.lowerBound * that.lowerBound,
      this.lowerBound * that.upperBound,
      this.upperBound * that.lowerBound,
      this.upperBound * that.upperBound)

    Interval(products.min, products.max)
  }
  final def *(that: Interval): Interval = this.mul(that)

  final def div(that: Interval): Interval = {
    that match {
      case _ if that.lowerBound > 0.0 || that.upperBound < 0.0 => this.mul(Interval(1.0 / that.upperBound, 1.0 / that.lowerBound))
      case _ if that.lowerBound == 0.0 => this.mul(Interval(1.0 / that.upperBound, java.lang.Double.POSITIVE_INFINITY))
      case _ if that.upperBound == 0.0 => this.mul(Interval(java.lang.Double.NEGATIVE_INFINITY, 1 / that.lowerBound))
      case _ => Interval(java.lang.Double.NEGATIVE_INFINITY, java.lang.Double.POSITIVE_INFINITY)
    }
  }
  final def /(that: Interval): Interval = this.div(that)

  final def moveBy(delta: java.lang.Double): Interval = this.add(Interval(delta))

  final def constrain(min: java.lang.Double, max: java.lang.Double): Interval = {
    def check(value: java.lang.Double) =
      if (value < min) min
      else {
        if (value > max) max
        else value
      }
    Interval(check(lowerBound), check(upperBound))
  }

  def split(ratios: Seq[java.lang.Double]): Seq[Interval] = {
    val sum = ratios.map(_.doubleValue()).sum
    ratios.tail.foldLeft(Seq(Interval(this.lowerBound, this.lowerBound + ratios.head * this.width / sum))) {
      case (result, r) => {
        val lastInterval = result.head
        val newInterval = Interval(lastInterval.upperBound, lastInterval.upperBound + r * this.width / sum)
        newInterval +: result
      }
    }.reverse
  }

  def bisect(): (Interval, Interval) = {
    val Seq(first, second) = split(ratios = Seq(1.0, 1.0))
    (first, second)
  }

}

object Interval {

  import Converters._

  var minWidth: java.lang.Double = 1e-5

  final def apply(lowerBound: java.lang.Double, upperBound: java.lang.Double): Interval = {
    if (lowerBound > upperBound) throw new MinMaxFailureException(lowerBound, upperBound)
    else {
      if (upperBound.doubleValue() - lowerBound < minWidth) Interval(0.5 * (lowerBound.doubleValue() + upperBound))
      else new Interval(lowerBound, upperBound)
    }
  }

  final def apply(value: java.lang.Double): Interval = value

  object Converters {

    implicit def fromDoubleScala(value: Double): Interval = new Interval(value, value)

    implicit def fromDouble(value: java.lang.Double): Interval = new Interval(value, value)

    implicit def fromString(value: String): Interval = {
      val split = value.drop(1).dropRight(1).split(";")
      if (split.length == 2) Interval(split(0).toDouble, split(1).toDouble)
      else fromDouble(value.toDouble)
    }

    implicit def fromPairScala(pair: (Double, Double)): Interval = Interval(pair._1, pair._2)

    implicit def fromPair(pair: (java.lang.Double, java.lang.Double)): Interval = Interval(pair._1, pair._2)

  }

  object Exceptions {

    class MinMaxFailureException(min: java.lang.Double, max: java.lang.Double) extends Exception

    class UnknownOperationException(opName: String) extends Exception

    class BadAreaOperationException(opName: String, interval: Interval) extends Exception

  }

  implicit object IntervalJsonFormat extends RootJsonFormat[Interval] {
    def write(i: Interval) = JsObject(
      "Interval" -> JsObject(
        "lower_bound" -> JsNumber(i.lowerBound),
        "upper_bound" -> JsNumber(i.upperBound)))

    def read(json: JsValue): Interval =
      json.asJsObject.getFields("Interval") match {
        case Seq(interval) => interval.asJsObject.getFields("lower_bound", "upper_bound") match {
          case Seq(JsNumber(lowerBound), JsNumber(upperBound)) =>
            Interval(lowerBound.toDouble, upperBound.toDouble)
          case _ => throw DeserializationException("No necessary fields")
        }
        case _ => throw DeserializationException("No Interval Field")
      }
  }

}