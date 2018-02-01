package kaimere.real.optimization.classic.zero_order

import kaimere.real.optimization._
import kaimere.real.optimization.general._
import kaimere.real.optimization.general.instructions._
import org.scalatest.FunSuite
import spray.json._

class RandomSearchSuite extends FunSuite {

  private val epsNorm = 1e-2
  private val maxTries = 5
  private val maxTime = 0.5
  private val maxIterations = 1000

  private val config = "{ \"name\": \"RandomSearch\", \"numberOfAttempts\": 10, \"deltaRatio\": 0.001 }".parseJson
  private val RS: OptimizationAlgorithm = OptimizationAlgorithm.fromJson(config)

  test("Serialization") {
    assert(RS.asInstanceOf[RandomSearch].toJson.convertTo[RandomSearch] == RS.asInstanceOf[RandomSearch])
  }


  test("Dummy #1 (by max time)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      state = None,
      instruction = VerboseBest(MaxTime(1 * maxTime)),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #1 (by target value)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      state = Some(Vector(Map("x" -> 10.0))),
      instruction = TargetValue(targetValue = 0.0),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #2 (by max time)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_2,
      area = DummyFunctions.area_2,
      state = None,
      instruction = MaxTime(2 * maxTime),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #2 (by max iterations)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_2,
      area = DummyFunctions.area_2,
      state = Option(Vector(Map("x" -> 10.0, "y" -> -10.0))),
      instruction = MaxIterations(2 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #3 (by max time)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_3,
      area = DummyFunctions.area_3,
      state = None,
      instruction = MaxTime(3 * maxTime),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #3 (by max iterations)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_3,
      area = DummyFunctions.area_3,
      state = Option(Vector(Map("x" -> 10.0, "y" -> -10.0, "z" -> 10.0))),
      instruction = MaxIterations(3 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

}
