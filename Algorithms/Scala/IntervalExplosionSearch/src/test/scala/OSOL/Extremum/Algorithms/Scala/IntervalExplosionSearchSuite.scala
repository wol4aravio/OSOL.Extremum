package OSOL.Extremum.Algorithms.Scala

import OSOL.Extremum.Cores.JVM.Optimization.Testing.IntervalTester
import org.scalatest.FunSuite

class IntervalExplosionSearchSuite extends FunSuite {

  val r: Double = 1.0
  val maxBombs: Int = 10
  val oneMin: Double = 60.0

  test("Test Explosion Search")
  {
    val tester = new IntervalTester
    assert(tester(
      IntervalExplosionSearch.createIntervalExplosionSearch(maxBombs = 1 * maxBombs, rMax = Map("x" -> r, "y" -> r, "z" -> r), maxTime = 1 * oneMin),
      IntervalExplosionSearch.createIntervalExplosionSearch(maxBombs = 2 * maxBombs, rMax = Map("x" -> 0.5 * r, "y" -> 0.5 * r, "z" -> 0.5 * r), maxTime = 2 * oneMin),
      IntervalExplosionSearch.createIntervalExplosionSearch(maxBombs = 3 * maxBombs, rMax = Map("x" -> 0.1 * r, "y" -> 0.1 * r, "z" -> 0.1 * r), maxTime = 5 * oneMin)))
  }

}