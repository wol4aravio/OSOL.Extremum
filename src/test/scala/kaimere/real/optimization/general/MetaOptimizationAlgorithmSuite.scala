package kaimere.real.optimization.general

import kaimere.real.optimization._
import kaimere.real.optimization.general.instructions._
import kaimere.real.optimization.classic.zero_order.RandomSearch
import org.scalatest.FunSuite

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

  test("Serialization") {
    assert(OptimizationAlgorithm.fromJson(OptimizationAlgorithm.toJson(MOA)).asInstanceOf[MetaOptimizationAlgorithm] == MOA.asInstanceOf[MetaOptimizationAlgorithm])
  }


  test("Dummy #4 (by max time)") {

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

