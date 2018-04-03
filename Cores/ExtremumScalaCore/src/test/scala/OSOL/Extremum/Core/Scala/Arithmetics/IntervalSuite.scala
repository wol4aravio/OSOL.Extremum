package OSOL.Extremum.Core.Scala.Arithmetics

import org.scalatest.FunSuite
import spray.json._

import Interval._
import Interval.Converters._
import Interval.Exceptions._

class IntervalSuite extends FunSuite {

  val i1 = Interval(-1.0, 2.0)
  val i2 = Interval(-4.0, 3.0)
  val i3 = Interval(1.0, 2.0)
  val i4 = Interval(5.0, 5.1)
  val i5 = Interval(-6.0, -5.0)
  val i6 = Interval(-2.0, 0.0)
  val i7 = Interval(0.0, 3.0)

  test("To String") {
    assert(i1.toString == "[-1.0; 2.0]")
    assert(i4.toString == "[5.0; 5.1]")
    assert(i7.toString == "[0.0; 3.0]")
  }

  test("From String") {
    assert(i1 ~ "[-1.0; 2.0]")
    assert(i4 ~ "[5.0; 5.1]")
    assert(Interval(2.0) ~ "2.0")
    intercept[MinMaxFailureException] { Interval(3.0, 2.0) }
  }

  test("Interval Characteristics: Middlepoint") {
    assert(i1.middlePoint == 0.5)
    assert(i3.middlePoint == 1.5)
    assert(i7.middlePoint == 1.5)
  }

  test("Interval Characteristics: Width") {
    assert(i1.width == 3.0)
    assert(i3.width == 1.0)
    assert(i7.width == 3.0)
  }

  test("Interval Characteristics: Radius") {
    assert(i1.radius == 1.5)
    assert(i3.radius == 0.5)
    assert(i7.radius == 1.5)
  }

  test("Interval: ToString()") {
    assert(i1.toString == "[-1.0; 2.0]")
    assert(i2.toString == "[-4.0; 3.0]")
    assert(i5.toString == "[-6.0; -5.0]")
  }

  test("Approximate Equality") {
    assert(i1 ~ (i1 + 1e-7))
    assert(!(Interval(Double.NegativeInfinity, 0.0) ~ Interval(Double.NegativeInfinity, Double.NaN)))
  }

  test("Binary Arithmetic Operations: \"+\"") {
    assert((i1 + i2) ~ Interval(-5.0, 5.0))
    assert((i2 + i3) ~ Interval(-3.0, 5.0))
    assert((i5 + i4) ~ Interval(-1.0, 0.1))
  }

  test("Binary Arithmetic Operations: \"-\"") {
    assert((i1 - i2) ~ Interval(-4.0, 6.0))
    assert((i2 - i3) ~ Interval(-6.0, 2.0))
    assert((i5 - i4) ~ Interval(-11.1, -10.0))
  }

  test("Binary Arithmetic Operations: \"*\"") {
    assert((i1 * i2) ~ Interval(-8.0, 6.0))
    assert((i2 * i3) ~ Interval(-8.0, 6.0))
    assert((i5 * i4) ~ Interval(-30.6, -25.0))
  }

  test("Binary Arithmetic Operations: \"/\"") {
    assert((i1 / i2) ~ Interval(Double.NegativeInfinity, Double.PositiveInfinity))
    assert((i2 / i3) ~ Interval(-4.0, 3.0))
    assert((i1 / i5) ~ Interval(-0.4, 0.2))
    assert((i3 / i6) ~ Interval(Double.NegativeInfinity, -0.5))
    assert((i5 / i7) ~ Interval(Double.NegativeInfinity, -5.0 / 3.0))
  }

  test("Binary Arithmetic Operations: \"^\"") {
    assert((i1 ** 2.0) ~ Interval(0.0, 4.0))
    assert((i2 ^ 3.0) ~ Interval(-64.0, 27.0))
    assert((i5 ** 0.0) ~ Interval(1.0, 1.0))
  }

  test("Unary Operators: Neg") {
    assert((-i1) ~ Interval(-2.0, 1.0))
    assert((-i5) ~ Interval(5.0, 6.0))
    assert((-i6) ~ Interval(0.0, 2.0))
  }

  test("Unary Operators: Sin") {
    assert(i1.sin() ~ Interval(math.sin(-1.0), 1.0))
    assert(i2.sin() ~ Interval(-1.0, 1.0))
    assert(i3.sin() ~ Interval(math.sin(1.0), 1.0))
    assert(i6.sin() ~ Interval(-1.0, 0.0))
  }

  test("Unary Operators: Cos") {
    assert(i1.cos() ~ Interval(math.cos(2.0), 1.0))
    assert(i2.cos() ~ Interval(-1.0, 1.0))
    assert(i3.cos() ~ Interval(math.cos(2.0), math.cos(1.0)))
    assert(i6.cos() ~ Interval(math.cos(-2.0), 1.0))
  }

  test("Unary Operators: Abs") {
    assert(i1.abs() ~ Interval(0.0, 2.0))
    assert(i2.abs() ~ Interval(0.0, 4.0))
    assert(i3.abs() ~ Interval(1.0, 2.0))
    assert(i4.abs() ~ Interval(5.0, 5.1))
    assert(i5.abs() ~ Interval(5.0, 6.0))
    assert(i6.abs() ~ Interval(0.0, 2.0))
    assert(i7.abs() ~ Interval(0.0, 3.0))
  }

  test("Unary Operators: Exp") {
    assert(i1.exp() ~ Interval(math.exp(-1.0), math.exp(2.0)))
    assert(i2.exp() ~ Interval(math.exp(-4.0), math.exp(3.0)))
    assert(i3.exp() ~ Interval(math.exp(1.0), math.exp(2.0)))
  }

  test("Unary Operators: Sqrt") {
    assert(i1.sqrt() ~ Interval(0.0, math.sqrt(2.0)))
    assert(i3.sqrt() ~ Interval(math.sqrt(1.0), math.sqrt(2.0)))
    intercept[BadAreaOperationException] { i5.sqrt() }
  }

  test("Unary Operators: Ln") {
    assert(i1.ln() ~ Interval(Double.NegativeInfinity, math.log(2.0)))
    assert(i2.ln() ~ Interval(Double.NegativeInfinity, math.log(3.0)))
    assert(i3.ln() ~ Interval(math.log(1.0), math.log(2.0)))
    assert(i4.ln() ~ Interval(math.log(5.0), math.log(5.1)))
    intercept[BadAreaOperationException] { i5.ln() }
    assert(i6.ln() ~ Interval(Double.NegativeInfinity, Double.NegativeInfinity))
    assert(i7.ln() ~ Interval(Double.NegativeInfinity, math.log(3.0)))
  }

  test("Conversion: From Double") {
    assert(Interval(1.0, 1.0) ~ 1.0)
  }

  test("Conversion: From Tuple") {
    assert(Interval(-3.0, 1.0) ~ ((-3.0, 1.0)))
  }

  test("Move") {
    assert(i1.moveBy(1.0) == i7)
    assert(i7.moveBy(-1.0) == i1)
    assert(i5.moveBy(0.5) == Interval(-5.5, -4.5))
  }

  test("Recover") {
    val min = -0.7
    val max = 1.5
    assert(i1.constrain(min, max) == Interval(min, max))
    assert(i3.constrain(min, max) == Interval(1.0, max))
    assert(i4.constrain(min, max) == Interval(max, max))
    assert(i5.constrain(min, max) == Interval(min, min))
  }

  test("Splitting") {
    assert(i1.bisect()._1 ~ Interval(-1.0, 0.5))
    assert(i1.bisect()._2 ~ Interval(0.5, 2.0))
    assert(i1.split(Seq(1, 2)).zip(Seq(Interval(-1.0, 0.0), Interval(0.0, 2.0))).forall { case (a, b) => a ~ b })
  }

  test("JSON") {
    assert(i1.toJson.convertTo[Interval] == i1)
    assert(i2.toJson.convertTo[Interval] == i2)
    assert(i3.toJson.convertTo[Interval] == i3)
    intercept[DeserializationException]
      { i1.toJson.prettyPrint.replace("Interval", "Intervall").parseJson.convertTo[Interval] }
    intercept[DeserializationException]
      { i1.toJson.prettyPrint.replace("lowerBound", "a").replace("upperBound", "b").parseJson.convertTo[Interval] }
  }

}