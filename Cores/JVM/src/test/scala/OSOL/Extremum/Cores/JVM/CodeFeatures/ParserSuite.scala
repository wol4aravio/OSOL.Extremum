package OSOL.Extremum.Cores.JVM.CodeFeatures

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser.TreeFunctions._
import OSOL.Extremum.Cores.JVM.Random.GoRN
import OSOL.Extremum.Cores.JVM.Vectors._
import OSOL.Extremum.Cores.JVM.Random.GoRN
import org.scalatest.FunSuite
import OSOL.Extremum.Cores.JVM.Vectors.RealVector.Converters._
import OSOL.Extremum.Cores.JVM.Vectors.IntervalVector.Converters._

class ParserSuite extends FunSuite {

  val N = 100
  val tol = 1e-9
  val str = "-x - 1.0 + (sin(y) + cos(y)) * (exp(-x) + ln(10 - y)) / (abs(-3.0) ** sqrt(4.0))"
  val fDouble = (v: Map[String, Double]) => -v("x") - 1.0 + (math.sin(v("y"))+ math.cos(v("y"))) * (math.exp(-v("x")) + math.log(10.0 - v("y"))) / math.pow(math.abs(-3.0), math.sqrt(4.0))
  val fInterval = (v: Map[String, Interval]) => -v("x") - Interval(1.0) + (v("y").sin()+ v("y").cos()) * ((-v("x")).exp() + (Interval(10.0) - v("y")).log()) / (Interval(-3.0).abs() ** Interval(4.0).sqrt())

  test("DoubleTreeFunction") {
    val f = DoubleTreeFunction(str)
    val testPoints = (1 to N).map(_ => GoRN.getContinuousUniform(Seq("x", "y", "z").map(k => (k, (-1.0, 1.0))).toMap)).map(v => RealVector(v))
    assert(testPoints.forall(x => math.abs(fDouble(x.elements) - f(x)) < tol))
    val v: RealVector = Map("x" -> 1.0, "y" -> 2.0, "z" -> 3.0)
    val v1: RealVector = Map("x" -> v("x"))
    val v2: RealVector = Map("y" -> v("y"))
    val v3: RealVector = Map("z" -> v("z"))
    assert(f(v1, v2, v3) == f(v))
  }

  test("IntervalTreeFunction") {
    val f = IntervalTreeFunction(str)
    val testPoints = (1 to N).map(_ => GoRN.getContinuousUniform(Seq("x", "y", "z").map(k => (k, (-1.0, 1.0))).toMap)).map(_.mapValues(Interval(_))).map(v => IntervalVector(v))
    assert(testPoints.forall(x => (fInterval(x.elements) - f(x)).abs().middlePoint < tol))
    val v: IntervalVector = Map("x" -> Interval(1.0), "y" -> Interval(2.0, 3.0), "z" -> Interval(3.0, 5.0))
    val v1: IntervalVector = Map("x" -> v("x"))
    val v2: IntervalVector = Map("y" -> v("y"))
    val v3: IntervalVector = Map("z" -> v("z"))
    assert(f(v1, v2, v3) == f(v))
  }

}
