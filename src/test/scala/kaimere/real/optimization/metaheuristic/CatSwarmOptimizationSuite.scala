package kaimere.real.optimization.metaheuristic

import kaimere.real.optimization._
import kaimere.real.optimization.general._
import kaimere.real.optimization.general.instructions._
import org.scalatest.FunSuite
import spray.json._

class CatSwarmOptimizationSuite extends FunSuite {

  private val epsNorm = 1e-2
  private val maxTries = 10
  private val maxTime = 0.5
  private val maxIterations = 2500

  private val config = "CatSwarmOptimization,10,0.5,5,0.01,2,true,0.7,0.1"
  private val CSO: OptimizationAlgorithm = OptimizationAlgorithm.fromCsv(config)

  test("Serialization") {
    assert(OptimizationAlgorithm.fromJson(OptimizationAlgorithm.toJson(CSO)).asInstanceOf[CatSwarmOptimization] == CSO.asInstanceOf[CatSwarmOptimization])
  }


  test("Dummy #1 (by max time)") {

    val passed = Tester(
      tool = CSO,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      state = None,
      instruction = MaxTime(1 * maxTime),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #1 (by max iterations)") {

    val passed = Tester(
      tool = CSO,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      state = Some(Vector(Map("x" -> 10.0))),
      instruction = MaxIterations(1 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #2 (by max time)") {

    val passed = Tester(
      tool = CSO,
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
      tool = CSO,
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
      tool = CSO,
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
      tool = CSO,
      f = DummyFunctions.func_3,
      area = DummyFunctions.area_3,
      state = Some(Vector(Map("x" -> 10.0, "y" -> -10.0, "z" -> 10.0))),
      instruction = MaxIterations(3 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

}

