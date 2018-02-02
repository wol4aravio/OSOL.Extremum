package kaimere.real.optimization.general

import kaimere.real.optimization._
import kaimere.real.optimization.general.instructions._
import kaimere.real.optimization.classic.zero_order.RandomSearch
import org.scalatest.FunSuite
import spray.json._

class MetaOptimizationAlgorithmSuite extends FunSuite {

  private val epsNorm = 1e-2
  private val maxTries = 10
  private val maxTime = 2.5
  private val maxIterations = 1000

  private val rs: OptimizationAlgorithm = RandomSearch(10, 0.001)
  private val MOA: OptimizationAlgorithm = MetaOptimizationAlgorithm(
    algorithms = Seq(rs, rs, rs, rs, rs),
    targetVars = Seq(Some(Set("x")), Some(Set("a")), Some(Set("y")), Some(Set("b")), Some(Set("z", "c"))),
    instructions = Seq(VerboseBest(MaxIterations(maxIterations)), MaxIterations(maxIterations, verbose = true), VerboseBest(MaxTime(maxTime)), MaxTime(maxTime, verbose = true), TargetValue(targetValue = 0.00001, verbose = true)))

  test("Algorithm Serialization") {
    assert(OptimizationAlgorithm.fromJson(OptimizationAlgorithm.toJson(MOA)).asInstanceOf[MetaOptimizationAlgorithm] == MOA.asInstanceOf[MetaOptimizationAlgorithm])
  }

  test("State Serialization") {

    MOA.initialize(DummyFunctions.func_4, DummyFunctions.area_4)
    val result = MOA.work(MaxTime(1 * maxTime))

    assert(MOA.currentState.toJson.convertTo[State].getBestBy(DummyFunctions.func_4)._1 == result)

  }


  test("Dummy #4 (by max time, with initial State)") {

    val passed = Tester(
      tool = MOA,
      f = DummyFunctions.func_4,
      area = DummyFunctions.area_4,
      state = Some(Vector(Map("x" -> 10.0, "y" -> 10.0, "z" -> 10.0, "a" -> -10.0, "b" -> -10.0, "c" -> -10.0))),
      instruction = null,
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

  test("Dummy #4 (by max time, without initial State)") {

    val passed = Tester(
      tool = MOA,
      f = DummyFunctions.func_4,
      area = DummyFunctions.area_4,
      state = None,
      instruction = null,
      epsNorm = epsNorm,
      maxTries = maxTries)

    assert(passed)

  }

}

