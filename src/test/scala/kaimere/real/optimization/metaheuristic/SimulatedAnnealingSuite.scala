package kaimere.real.optimization.metaheuristic

import kaimere.real.optimization.general._
import kaimere.real.optimization.general.OptimizationAlgorithm.MergeStrategy
import kaimere.real.optimization._
import org.scalatest.FunSuite
import spray.json._

class SimulatedAnnealingSuite extends FunSuite {

  private val epsNorm = 1e-2
  private val maxTries = 10
  private val maxTime = 0.5
  private val maxIterations = 2500

  private val config = "{ \"name\": \"SimulatedAnnealing\", \"alpha\": 0.995, \"beta\": 1.0, \"gamma\": 1.0, \"initialTemp\": 500.0 }".parseJson
  private val SA: OptimizationAlgorithm = OptimizationAlgorithm.fromJson(config)

  test("Dummy #1 (by max time)") {

    val passed = Tester(
      tool = SA,
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
      tool = SA,
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
      tool = SA,
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
      tool = SA,
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
      tool = SA,
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
      tool = SA,
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

