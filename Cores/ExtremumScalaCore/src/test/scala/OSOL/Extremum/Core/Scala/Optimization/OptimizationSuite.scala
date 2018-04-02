package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Optimization.Exceptions.ParameterAlreadyExistsException
import OSOL.Extremum.Core.Scala.Optimization.Nodes.{GeneralNode, TerminationViaMaxIterations, TerminationViaMaxTime}
import OSOL.Extremum.Core.Scala.Random.GoRN
import OSOL.Extremum.Core.Scala.Arithmetics.Interval
import OSOL.Extremum.Core.Scala.Vectors.{IntervalVector, RealVector}
import OSOL.Extremum.Core.Scala.Vectors.RealVector.Converters._
import org.scalatest.FunSuite

class OptimizationSuite extends FunSuite {

  object DummyRealOptimization {

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

  val toolReal: Algorithm[RealVector, Double, RealVector] = DummyRealOptimization()
  val toolInterval: Algorithm[IntervalVector, Interval, IntervalVector] = DummyIntervalOptimization()
  val fReal: Map[String, Double] => Double = (v: Map[String, Double]) => math.abs(v("x"))
  val fInterval: Map[String, Interval] => Interval = (v: Map[String, Interval]) => v("x").abs()
  val area: Area = Map("x" -> (-10.0, 10.0))
  val eps = 1e-3

  test("TerminationViaMaxIterations") {
    val node = new TerminationViaMaxIterations[RealVector, Double, RealVector](nodeId = 1, maxIteration = 250)
    val state: State[RealVector, Double, RealVector] = new State[RealVector, Double, RealVector]()

    node.initialize(fReal, area, state)
    intercept[ParameterAlreadyExistsException] { node.initialize(fReal, area, state) }
  }
  test("TerminationViaMaxTime") {
    val node = new TerminationViaMaxTime[IntervalVector, Interval, IntervalVector](nodeId = 1, maxTime = 1.0)
    val state: State[IntervalVector, Interval, IntervalVector] = new State[IntervalVector, Interval, IntervalVector]()

    node.initialize(fInterval, area, state)
    intercept[ParameterAlreadyExistsException] { node.initialize(fInterval, area, state) }
  }

  test("Test #1") {
    val result = toolReal.work(fReal, area)
    assert(math.abs(result("x")) < eps)
  }

  test("Test #2") {
    val result = toolInterval.work(fInterval, area)
    assert(math.abs(result("x").middlePoint) < eps)
  }

}
