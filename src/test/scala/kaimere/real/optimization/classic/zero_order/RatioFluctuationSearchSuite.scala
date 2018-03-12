package kaimere.real.optimization.classic.zero_order

import kaimere.real.optimization.OptimizationTestHelper._
import kaimere.real.optimization.general._
import kaimere.real.optimization.general.State._
import kaimere.real.optimization.general.initializers.PureRandomInitializer
import kaimere.real.optimization.general.instructions._
import org.scalatest.FunSuite
import spray.json._

class RatioFluctuationSearchSuite extends FunSuite {

  private val epsNorm = 1e-2
  private val maxTries = 5
  private val maxTime = 0.5
  private val maxIterations = 1000

  private val config = "RatioFluctuationSearch,10,0.01"
  private val RFS: OptimizationAlgorithm = OptimizationAlgorithm.fromCsv(config)

  test("Algorithm Serialization") {
    assert(OptimizationAlgorithm.fromJson(OptimizationAlgorithm.toJson(RFS)).asInstanceOf[RatioFluctuationSearch] == RFS.asInstanceOf[RatioFluctuationSearch])
  }


  test("State Serialization") {

    RFS.initialize(DummyFunctions.func_1, DummyFunctions.area_1, initializer = PureRandomInitializer())
    val result = RFS.work(MaxTime(1 * maxTime))

    assert(RFS.currentState.toJson.convertTo[State].getBestBy(DummyFunctions.func_1)._1 == result)

  }

  test("Dummy #1 (by max time)") {

    val passed = Tester(
      tool = RFS,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      defaultValues = None,
      instruction = MaxTime(1 * maxTime),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #1 (by max iterations)") {

    val passed = Tester(
      tool = RFS,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      defaultValues = Some((10.0, Seq.empty[(String, Double)])),
      instruction = MaxIterations(1 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #2 (by max time)") {

    val passed = Tester(
      tool = RFS,
      f = DummyFunctions.func_2,
      area = DummyFunctions.area_2,
      defaultValues = None,
      instruction = MaxTime(2 * maxTime),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #2 (by max iterations)") {

    val passed = Tester(
      tool = RFS,
      f = DummyFunctions.func_2,
      area = DummyFunctions.area_2,
      defaultValues = Some((10.0, Seq.empty[(String, Double)])),
      instruction = MaxIterations(2 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #3 (by max time)") {

    val passed = Tester(
      tool = RFS,
      f = DummyFunctions.func_3,
      area = DummyFunctions.area_3,
      defaultValues = None,
      instruction = MaxTime(3 * maxTime),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #3 (by max iterations)") {

    val passed = Tester(
      tool = RFS,
      f = DummyFunctions.func_3,
      area = DummyFunctions.area_3,
      defaultValues = Some((10.0, Seq.empty[(String, Double)])),
      instruction = MaxIterations(3 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

}
