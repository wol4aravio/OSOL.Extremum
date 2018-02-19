package kaimere.real.optimization.general

import java.io.File

import kaimere.real.optimization.OptimizationTestHelper._
import kaimere.real.optimization.general.instructions._
import kaimere.real.optimization.classic.zero_order.RandomSearch
import kaimere.real.optimization.general.initializers.PureRandomInitializer
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
    instructions = Seq(
      VerboseBest(MaxIterations(maxIterations)),
      AnyInstruction(MaxIterations(maxIterations, verbose = true), MaxTime(0.1 * maxTime)),
      VerboseBest(MaxTime(maxTime)),
      AllInstruction(MaxTime(maxTime * 2, verbose = true), MaxTime(maxTime, verbose = true)),
      TargetValue(targetValue = 0.00001, verbose = true)))

  test("Algorithm Serialization") {
    assert(OptimizationAlgorithm.fromJson(OptimizationAlgorithm.toJson(MOA)).asInstanceOf[MetaOptimizationAlgorithm] == MOA.asInstanceOf[MetaOptimizationAlgorithm])
  }

  test("State Serialization") {

    MOA.initialize(DummyFunctions.func_4, DummyFunctions.area_4, initializer = PureRandomInitializer(25))
    val result = MOA.work(MaxTime(1 * maxTime))
    val vectors: Vector[Map[String, Double]] = MOA.currentState.toJson.convertTo[State]

    assert(vectors.minBy(DummyFunctions.func_4(_)) == result.vals)

  }


  test("Dummy #4 (by max time, with initial State)") {

    val passed = Tester(
      tool = MOA,
      f = DummyFunctions.func_4,
      area = DummyFunctions.area_4,
      defaultValues = Some((10.0, Seq.empty[(String, Double)])),
      instruction = StateLogger(folderName = "./tmp", mainInstruction = null, bestOnly = true),
      epsNorm = epsNorm,
      maxTries = maxTries)

    StateLogger.deleteFolder(new File("./tmp"))

    assert(passed)

  }

  test("Dummy #4 (by max time, without initial State)") {

    val passed = Tester(
      tool = MOA,
      f = DummyFunctions.func_4,
      area = DummyFunctions.area_4,
      defaultValues = None,
      instruction = StateLogger(folderName = "./tmp", mainInstruction = null, bestOnly = false),
      epsNorm = epsNorm,
      maxTries = maxTries)

    StateLogger.deleteFolder(new File("./tmp"))

    assert(passed)

  }

}

