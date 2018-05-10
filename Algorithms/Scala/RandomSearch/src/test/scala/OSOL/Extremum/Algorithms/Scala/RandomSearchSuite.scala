package OSOL.Extremum.Algorithms.Scala

import OSOL.Extremum.Cores.JVM.Optimization.Testing.RealTester
import org.scalatest.FunSuite

class RandomSearchSuite extends FunSuite {

  val r: Double = 1.0
  val oneMin: Double = 60.0

  test("Warm Up")
  {
    val tester = new RealTester
    try {
      val result = tester(
        RandomSearch.createFixedStepRandomSearch(radius = 1.0 * r, maxTime = 1 * oneMin),
        RandomSearch.createFixedStepRandomSearch(radius = 0.5 * r, maxTime = 2 * oneMin),
        RandomSearch.createFixedStepRandomSearch(radius = 0.1 * r, maxTime = 5 * oneMin))
    }
    finally {
      assert(true)
    }
  }

  test("Test Random Search")
  {
    val tester = new RealTester
    assert(tester(
      RandomSearch.createFixedStepRandomSearch(radius = 1.0 * r, maxTime = 1 * oneMin),
      RandomSearch.createFixedStepRandomSearch(radius = 0.5 * r, maxTime = 2 * oneMin),
      RandomSearch.createFixedStepRandomSearch(radius = 0.1 * r, maxTime = 5 * oneMin)))
  }

}
