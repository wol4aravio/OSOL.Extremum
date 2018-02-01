package kaimere.real.optimization.metaheuristic

import kaimere.real.optimization._
import kaimere.real.optimization.general._
import kaimere.real.optimization.general.instructions._
import org.scalatest.FunSuite
import spray.json._

class ExplosionSearchSuite extends FunSuite {

  private val epsNorm = 1e-2
  private val maxTries = 10
  private val maxTime = 0.5
  private val maxIterations = 2500

  private val config = "{ \"name\": \"ExplosionSearch\", \"numberOfBombs\": 10, \"powerRatio\": 0.01 }".parseJson
  private val ES: OptimizationAlgorithm = OptimizationAlgorithm.fromJson(config)

  test("Serialization") {
    assert(ES.asInstanceOf[ExplosionSearch].toJson.convertTo[ExplosionSearch] == ES.asInstanceOf[ExplosionSearch])
  }

  test("Dummy #1 (by max time)") {

    val passed = Tester(
      tool = ES,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      state = None,
      instruction = MaxTime(1 * maxTime),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #1 (by target value)") {

    val passed = Tester(
      tool = ES,
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
      tool = ES,
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
      tool = ES,
      f = DummyFunctions.func_2,
      area = DummyFunctions.area_2,
      state = Some(Vector(Map("x" -> 10.0, "y" -> -10.0))),
      instruction = MaxIterations(2 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #3 (by max time)") {

    val passed = Tester(
      tool = ES,
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
      tool = ES,
      f = DummyFunctions.func_3,
      area = DummyFunctions.area_3,
      state = Some(Vector(Map("x" -> 10.0, "y" -> -10.0, "z" -> 10.0))),
      instruction = MaxIterations(3 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

}

