package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Optimization.Testing.RealTester
import org.scalatest.FunSuite

class RandomSearchSuite extends FunSuite {

  val r: Double = 1.0
  val fiveSec: Double = 5.0

  test("Test Random Search")
  {
    val tester = new RealTester
    assert(tester(
      RandomSearch.createFixedStepRandomSearch(radius = r, maxTime = 1 * fiveSec),
      RandomSearch.createFixedStepRandomSearch(radius = r, maxTime = 2 * fiveSec),
      RandomSearch.createFixedStepRandomSearch(radius = r, maxTime = 3 * fiveSec)))
  }

}
