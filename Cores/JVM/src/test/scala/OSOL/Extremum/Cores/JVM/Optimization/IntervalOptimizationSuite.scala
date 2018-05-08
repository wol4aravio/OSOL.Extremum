package OSOL.Extremum.Cores.JVM.Optimization

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.Optimization.Exceptions.ParameterAlreadyExistsException
import OSOL.Extremum.Cores.JVM.Optimization.Nodes.{GeneralNode, SetParametersNode, TerminationViaMaxIterations, TerminationViaMaxTime}
import OSOL.Extremum.Cores.JVM.Optimization.Testing.{IntervalTester, RealTester}
import OSOL.Extremum.Cores.JVM.Random.GoRN
import OSOL.Extremum.Cores.JVM.Vectors.{IntervalVector, RealVector}
import org.scalatest.FunSuite

class IntervalOptimizationSuite extends FunSuite {

  object DummyIntervalOptimization {

    val parameterName = "sample"

    final class SplitNode(override val nodeId: Int) extends GeneralNode[IntervalVector, Interval, IntervalVector](nodeId) {

      override def initialize(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {
        state.setParameter(parameterName, IntervalVector(area.mapValues { case (a, b) => Interval(a, b)}))
      }

      override def process(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {
        val currentInterval = state.getParameter[IntervalVector](parameterName)
        val (left, right) = currentInterval.bisect()
        if (left.getPerformance(f) < right.getPerformance(f)) { state.setParameter(parameterName, left) }
        else { state.setParameter(parameterName, right) }
      }

    }

    final class SelectBest(override val nodeId: Int) extends GeneralNode[IntervalVector, Interval, IntervalVector](nodeId) {

      override def initialize(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = { }

      override def process(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {
        state.result = Some(state.getParameter[IntervalVector](parameterName))
      }

    }

    def apply(): Algorithm[IntervalVector, Interval, IntervalVector] = {
      val nodes = Seq(
        new SplitNode(nodeId = 0),
        new TerminationViaMaxIterations[IntervalVector, Interval, IntervalVector](nodeId = 1, maxIteration = 250),
        new TerminationViaMaxTime[IntervalVector, Interval, IntervalVector](nodeId = 2, maxTime = 2.5),
        new SelectBest(nodeId = 3)
      )
      val transitionMatrix = Seq(
        (0, None, 1),
        (1, Some(0), 0),
        (1, Some(1), 2),
        (2, Some(0), 0),
        (2, Some(1), 3)
      )
      new Algorithm[IntervalVector, Interval, IntervalVector](nodes, transitionMatrix)
    }

  }

  val toolInterval: Algorithm[IntervalVector, Interval, IntervalVector] = DummyIntervalOptimization()
  val testerInterval = new IntervalTester

  test("Dummy Test") {
    assert(testerInterval(toolInterval))
    Thread.sleep(5000)
  }

}
