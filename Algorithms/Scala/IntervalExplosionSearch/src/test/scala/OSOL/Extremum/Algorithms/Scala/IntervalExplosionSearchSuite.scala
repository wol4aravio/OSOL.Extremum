package OSOL.Extremum.Algorithms.Scala

import OSOL.Extremum.Cores.JVM.Optimization.Testing.IntervalTester
import org.scalatest.FunSuite

class IntervalExplosionSearchSuite extends FunSuite {

  val rMaxRatio: Double = 0.1
  val maxBombs: Int = 10
  val oneMin: Double = 60.0

  test("Test Explosion Search")
  {
    val tester = new IntervalTester
    assert(tester(
      IntervalExplosionSearch.createIntervalExplosionSearch(maxBombs = 1 * maxBombs, rMaxRatio = rMaxRatio, maxTime = 1 * oneMin),
      IntervalExplosionSearch.createIntervalExplosionSearch(maxBombs = 2 * maxBombs, rMaxRatio = 0.5 * rMaxRatio, maxTime = 2 * oneMin),
      IntervalExplosionSearch.createIntervalExplosionSearch(maxBombs = 3 * maxBombs, rMaxRatio = 0.1 * rMaxRatio, maxTime = 5 * oneMin)))
  }

}