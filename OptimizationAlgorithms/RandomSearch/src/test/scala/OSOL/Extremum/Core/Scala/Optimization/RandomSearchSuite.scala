package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Vectors.RealVector
import org.scalatest.FunSuite

class RandomSearchSuite extends FunSuite {

  val eps = 1e-5
  val r: Double = 1.0
  val fiveSec: Double = 5.0


  def getNorm(r: RealVector): Double = math.sqrt(r.elements.values.map(v => v * v).sum)

  test("Test # 1") {
    val tool: Algorithm[RealVector, Double, RealVector] = RandomSearch.createFixedStepRandomSearch(radius = r, maxTime = fiveSec)
    val f1: Map[String, Double] => Double = (v: Map[String, Double]) => v("x") * v("x")
    val a1: Area = Seq("x").map((_, (-10.0, 10.0))).toMap
    val r1: RealVector = tool.work(f1, a1)
    assert(getNorm(r1) <= eps)
  }

  test("Test # 2") {
    val tool: Algorithm[RealVector, Double, RealVector] = RandomSearch.createFixedStepRandomSearch(radius = r, maxTime = fiveSec)
    val f2: Map[String, Double] => Double = (v: Map[String, Double]) => v("x") * v("x") + v("y") * v("y")
    val a2: Area = Seq("x", "y").map((_, (-10.0, 10.0))).toMap
    val r2: RealVector = tool.work(f2, a2)
    assert(getNorm(r2) <= eps)
  }

  test("Test # 3") {
    val tool: Algorithm[RealVector, Double, RealVector] = RandomSearch.createFixedStepRandomSearch(radius = r, maxTime = fiveSec)
    val f3: Map[String, Double] => Double = (v: Map[String, Double]) => v("x") * v("x") + v("y") * v("y") + v("z") * v("z")
    val a3: Area = Seq("x", "y", "z").map((_, (-10.0, 10.0))).toMap
    val r3: RealVector = tool.work(f3, a3)
    assert(getNorm(r3) <= eps)
  }

}
