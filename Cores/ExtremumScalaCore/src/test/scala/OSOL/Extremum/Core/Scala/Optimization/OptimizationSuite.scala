package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Optimization.Exceptions.ParameterAlreadyExistsException
import OSOL.Extremum.Core.Scala.Optimization.Nodes.{GeneralNode, SetParametersNode, TerminationViaMaxIterations, TerminationViaMaxTime}
import OSOL.Extremum.Core.Scala.Random.GoRN
import OSOL.Extremum.Core.Scala.Arithmetics.Interval
import OSOL.Extremum.Core.Scala.Optimization.Testing.{IntervalTester, RealTester}
import OSOL.Extremum.Core.Scala.Vectors.{IntervalVector, RealVector}
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
        if (state.getParameter[Boolean]("generate")) {
          val newPoint: RealVector = alreadySampledPoints.headOption.getOrElse(RealVector(GoRN.getContinuousUniform(area)))
            .moveBy(GoRN.getContinuousUniform(area.mapValues { case _ => (-1.0, 1.0)}))
            .constrain(area)
          val sadasd = (newPoint +: alreadySampledPoints).sortBy(_.getPerformance(f)).take(9).map(x => (x, x.getPerformance(f)))
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

  val toolReal: Algorithm[RealVector, Double, RealVector] = DummyRealOptimization(250, 2.5)
  val toolInterval: Algorithm[IntervalVector, Interval, IntervalVector] = DummyIntervalOptimization()

  val fReal: Map[String, Double] => Double = (v: Map[String, Double]) => math.abs(v("x"))
  val fInterval: Map[String, Interval] => Interval = (v: Map[String, Interval]) => v("x").abs()
  val area: Area = Map("x" -> (-10.0, 10.0))

  val testerReal = new RealTester
  val testerInterval = new IntervalTester

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
    assert(try { val json = toolReal.serializeState(); true} catch { case _: Exception => false })
    assert(testerReal(DummyRealOptimization(250, 2.5), DummyRealOptimization(500, 5.0)))
  }

  test("Test #2") {
    val result = toolInterval.work(fInterval, area)
    assert(try { val json = toolInterval.serializeState(); true} catch { case _: Exception => false })
    assert(testerInterval(toolInterval))
  }

}
