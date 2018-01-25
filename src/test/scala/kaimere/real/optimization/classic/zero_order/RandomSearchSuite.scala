package kaimere.real.optimization.classic.zero_order

import kaimere.real.optimization.general._
import kaimere.real.optimization.general.OptimizationAlgorithm.MergeStrategy
import kaimere.real.optimization.{Tester, _}
import org.scalatest.FunSuite
import spray.json._

class RandomSearchSuite extends FunSuite {

  private val epsNorm = 1e-2
  private val maxTries = 5
  private val RS: OptimizationAlgorithm = OptimizationAlgorithm("{ \"name\": \"RandomSearch\", \"numberOfAttempts\": 10, \"deltaRatio\": 0.001 }".parseJson)

  test("Dummy #1 (by max time)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      state = Vector(Map("x" -> 10.0)),
      mergeStrategy = MergeStrategy.force,
      instruction = Instruction.MaxTime(1 * 2.5),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #1 (by max iterations)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_1,
      area = DummyFunctions.area_1,
      state = Vector(Map("x" -> 10.0)),
      mergeStrategy = MergeStrategy.force,
      instruction = Instruction.MaxIterations(1 * 1000),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #2 (by max time)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_2,
      area = DummyFunctions.area_2,
      state = Vector(Map("x" -> 10.0, "y" -> -10.0)),
      mergeStrategy = MergeStrategy.force,
      instruction = Instruction.MaxTime(2 * 2.5),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #2 (by max iterations)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_2,
      area = DummyFunctions.area_2,
      state = Vector(Map("x" -> 10.0, "y" -> -10.0)),
      mergeStrategy = MergeStrategy.force,
      instruction = Instruction.MaxIterations(2 * 1000),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #3 (by max time)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_3,
      area = DummyFunctions.area_3,
      state = Vector(Map("x" -> 10.0, "y" -> -10.0, "z" -> 10.0)),
      mergeStrategy = MergeStrategy.force,
      instruction = Instruction.MaxTime(3 * 2.5),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #3 (by max iterations)") {

    val passed = Tester(
      tool = RS,
      f = DummyFunctions.func_3,
      area = DummyFunctions.area_3,
      state = Vector(Map("x" -> 10.0, "y" -> -10.0, "z" -> 10.0)),
      mergeStrategy = MergeStrategy.force,
      instruction = Instruction.MaxIterations(3 * 1000),
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

}
