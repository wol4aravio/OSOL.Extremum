package OSOL.Extremum.Cores.JVM.Optimization

import OSOL.Extremum.Cores.JVM.Optimization.Exceptions.ParameterAlreadyExistsException
import OSOL.Extremum.Cores.JVM.Optimization.Nodes.{GeneralNode, SetParametersNode, TerminationViaMaxIterations, TerminationViaMaxTime}
import OSOL.Extremum.Cores.JVM.Random.GoRN
import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.Optimization.Testing.{IntervalTester, RealTester}
import OSOL.Extremum.Cores.JVM.Vectors.{IntervalVector, RealVector}
import OSOL.Extremum.Cores.JVM.Random.GoRN
import org.scalatest.FunSuite

class RealOptimizationSuite extends FunSuite {

  object DummyRealOptimization {

    val parameterName = "samples"

    final class SampleNode(override val nodeId: Int) extends GeneralNode[RealVector, Double, RealVector](nodeId) {

      override def initialize(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = {
        state.setParameter(parameterName, Seq.empty[RealVector])
      }

      override def process(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = {
        val alreadySampledPoints = state.getParameter[Seq[RealVector]](parameterName)
        if (state.getParameter[Boolean]("generate")) {
          val newPoint: RealVector = alreadySampledPoints.headOption.getOrElse(RealVector(GoRN.getContinuousUniform(area)))
            .moveBy(GoRN.getContinuousUniform(area.mapValues { case _ => (-0.1, 0.1)}))
            .constrain(area)
          state.setParameter(parameterName, (newPoint +: alreadySampledPoints).sortBy(_.getPerformance(f)).take(9))
        }
      }

    }

    final class SelectBest(override val nodeId: Int) extends GeneralNode[RealVector, Double, RealVector](nodeId) {

      override def initialize(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = { }

      override def process(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = {
        state.result = Some(state.getParameter[Seq[RealVector]](parameterName).minBy(_.getPerformance(f)))
      }

    }

    def apply(maxIteration: Int, maxTime: Double): Algorithm[RealVector, Double, RealVector] = {
      val nodes = Seq(
        new SetParametersNode[RealVector, Double, RealVector](nodeId = 0, parameters = Map("generate" -> true)),
        new SampleNode(nodeId = 1),
        new TerminationViaMaxIterations[RealVector, Double, RealVector](nodeId = 2, maxIteration = maxIteration),
        new TerminationViaMaxTime[RealVector, Double, RealVector](nodeId = 3, maxTime = maxTime),
        new SelectBest(nodeId = 4)
      )
      val transitionMatrix = Seq(
        (0, None, 1),
        (1, None, 2),
        (2, Some(0), 1),
        (2, Some(1), 3),
        (3, Some(0), 1),
        (3, Some(1), 4)
      )
      new Algorithm[RealVector, Double, RealVector](nodes, transitionMatrix)
    }

  }

  val testerReal = new RealTester

  test("Dummy Test") {
    assert(testerReal(DummyRealOptimization(100, 60.0), DummyRealOptimization(250, 150.0)))
    Thread.sleep(5000)
  }

}
