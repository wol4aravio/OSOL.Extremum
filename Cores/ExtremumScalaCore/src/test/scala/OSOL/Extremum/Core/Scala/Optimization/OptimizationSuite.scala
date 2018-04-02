package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Optimization.Nodes.{GeneralNode, TerminationViaMaxIterations, TerminationViaMaxTime}
import OSOL.Extremum.Core.Scala.Random.GoRN
import OSOL.Extremum.Core.Scala.Vectors.RealVector
import OSOL.Extremum.Core.Scala.Vectors.RealVector.Converters._
import org.scalatest.FunSuite

class OptimizationSuite extends FunSuite {

  object DummyOptimization {

    val parameterName = "samples"

    final class SampleNode(override val nodeId: Int) extends GeneralNode[RealVector, Double, RealVector](nodeId) {

      override def initialize(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = {
        state.setParameter(parameterName, Seq.empty[RealVector])
      }

      override def process(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = {
        val alreadySampledPoints = state.getParameter[Seq[RealVector]](parameterName)
        val newPoint: RealVector = GoRN.getContinuousUniform(area)
        state.setParameter(parameterName, newPoint +: alreadySampledPoints)
      }

    }

    final class SelectBest(override val nodeId: Int) extends GeneralNode[RealVector, Double, RealVector](nodeId) {

      override def initialize(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = { }

      override def process(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = {
        state.result = Some(state.getParameter[Seq[RealVector]](parameterName).minBy(_.getPerformance(f)))
      }

    }

    def apply(): Algorithm[RealVector, Double, RealVector] = {
      val nodes = Seq(
        new SampleNode(nodeId = 0),
        new TerminationViaMaxIterations[RealVector, Double, RealVector](nodeId = 1, maxIteration = 250),
        new TerminationViaMaxTime[RealVector, Double, RealVector](nodeId = 2, maxTime = 2.5),
        new SelectBest(nodeId = 3)
      )
      val transitionMatrix = Seq(
        (0, None, 1),
        (1, Some(0), 0),
        (1, Some(1), 2),
        (2, Some(0), 0),
        (2, Some(1), 3)
      )
      new Algorithm[RealVector, Double, RealVector](nodes, transitionMatrix)
    }

  }

  val tool = DummyOptimization()
  val eps = 1e-5

  test("Test #1") {

    val result = tool.work(
      f = (v: Map[String, Double]) => math.abs(v("x")),
      area = Map("x" -> (-10.0, 10.0))
    )

    assert(math.abs(result("x")) < eps)

  }

}
