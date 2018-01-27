package kaimere.real.optimization.metaheuristic

import kaimere.real.optimization.general._
import kaimere.real.optimization.general.OptimizationAlgorithm.MergeStrategy
import kaimere.real.optimization._
import org.scalatest.FunSuite
import spray.json._

class CatSwarmOptimizationSuite extends FunSuite {

  private val epsNorm = 1e-2
  private val maxTries = 10
  private val maxTime = 0.5
  private val maxIterations = 2500

  private val config = "{ \"name\": \"CatSwarmOptimization\", \"numberOfCats\": 10, \"MR\": 0.5, \"SMP\": 5, \"CDC\": 2, \"SRD\": 0.01, \"SPC\": true, \"velocityConstant\": 0.7, \"velocityRatio\": 0.1 }".parseJson
  private val CSO: OptimizationAlgorithm = OptimizationAlgorithm.fromJson(config)

  test("Dummy #1 (by max time)") {

    val passed = Tester(
      tool = CSO,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      state = null,
      mergeStrategy = MergeStrategy.selfInit,
      instruction = Instruction.MaxTime(1 * maxTime),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #1 (by max iterations)") {

    val passed = Tester(
      tool = CSO,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      state = Vector(Map("x" -> 10.0)),
      mergeStrategy = MergeStrategy.force,
      instruction = Instruction.MaxIterations(1 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #2 (by max time)") {

    val passed = Tester(
      tool = CSO,
      f = DummyFunctions.func_2,
      area = DummyFunctions.area_2,
      state = null,
      mergeStrategy = MergeStrategy.selfInit,
      instruction = Instruction.MaxTime(2 * maxTime),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #2 (by max iterations)") {

    val passed = Tester(
      tool = CSO,
      f = DummyFunctions.func_2,
      area = DummyFunctions.area_2,
      state = Vector(Map("x" -> 10.0, "y" -> -10.0)),
      mergeStrategy = MergeStrategy.force,
      instruction = Instruction.MaxIterations(2 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #3 (by max time)") {

    val passed = Tester(
      tool = CSO,
      f = DummyFunctions.func_3,
      area = DummyFunctions.area_3,
      state = null,
      mergeStrategy = MergeStrategy.selfInit,
      instruction = Instruction.MaxTime(3 * maxTime),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #3 (by max iterations)") {

    val passed = Tester(
      tool = CSO,
      f = DummyFunctions.func_3,
      area = DummyFunctions.area_3,
      state = Vector(Map("x" -> 10.0, "y" -> -10.0, "z" -> 10.0)),
      mergeStrategy = MergeStrategy.force,
      instruction = Instruction.MaxIterations(3 * maxIterations),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

}

