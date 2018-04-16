package OSOL.Extremum.Core.Scala.CodeFeatures

import OSOL.Extremum.Core.Scala.Arithmetics.Interval
import OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser.Parser
import OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser.TreeFunctions._
import OSOL.Extremum.Core.Scala.Random.GoRN
import OSOL.Extremum.Core.Scala.Vectors._
import org.scalatest.FunSuite

class ParserSuite extends FunSuite {

  val N = 100
  val tol = 1e-9
  val str = "x - 1.0 + (sin(y) + cos(y)) * (exp(-x) + ln(10 + -y)) / (abs(-3.0) ^ sqrt(4.0))"
  val fDouble = (v: Map[String, Double]) => v("x") - 1.0 + (math.sin(v("y"))+ math.cos(v("y"))) * (math.exp(-v("x")) + math.log(10.0 - v("y"))) / math.pow(math.abs(-3.0), math.sqrt(4.0))
  val fInterval = (v: Map[String, Interval]) => v("x") - Interval(1.0) + (v("y").sin()+ v("y").cos()) * ((-v("x")).exp() + (Interval(10.0) - v("y")).ln()) / (Interval(-3.0).abs() ** Interval(4.0).sqrt())

  test("Split to tokens") {
    val tokens = str |> Parser.ParserMethods.prepare |> Parser.ParserMethods.toTokens
    val desiredTokens = Array("x", "-", "1.0", "+", "(", "sin", "(", "y", ")", "+", "cos", "(", "y", ")", ")", "*", "(", "exp", "(", "~", "x", ")", "+", "ln", "(", "10", "-", "y", ")", ")", "/", "(", "abs", "(", "~", "3.0", ")", "^", "sqrt", "(", "4.0", ")", ")")
    assert(tokens.zip(desiredTokens).forall{ case (s1, s2) => s1.equals(s2) })
  }

  test("DoubleTreeFunction") {
    val f = DoubleTreeFunction(str)
    val testPoints = (1 to N).map(_ => GoRN.getContinuousUniform(Seq("x", "y", "z").map(k => (k, (-1.0, 1.0))).toMap)).map(v => RealVector(v))
    assert(testPoints.forall(x => fDouble(x.elements) - f(x) < tol))
  }

  test("IntervalTreeFunction") {
    val f = IntervalTreeFunction(str)
    val testPoints = (1 to N).map(_ => GoRN.getContinuousUniform(Seq("x", "y", "z").map(k => (k, (-1.0, 1.0))).toMap)).map(_.mapValues(Interval(_))).map(v => IntervalVector(v))
    assert(testPoints.forall(x => (fInterval(x.elements) - f(x)).middlePoint < tol))
  }

}
