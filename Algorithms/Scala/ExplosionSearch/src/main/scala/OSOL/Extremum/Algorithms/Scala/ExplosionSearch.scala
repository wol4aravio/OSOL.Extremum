package OSOL.Extremum.Algorithms.Scala

import OSOL.Extremum.Cores.JVM.Pipe
import OSOL.Extremum.Cores.JVM.Optimization._
import OSOL.Extremum.Cores.JVM.Optimization.Nodes.{GeneralNode, SetParametersNode, TerminationViaMaxTime}
import OSOL.Extremum.Cores.JVM.Random.GoRN
import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.Vectors.IntervalVector
import OSOL.Extremum.Cores.JVM.Vectors.IntervalVector.Converters._

object ExplosionSearch {

  private val maxBombsName = "maxBombs"
  private val maxPowerName = "maxPower"
  private val bombsName = "bombs"
  private val rMaxName = "rMax"

  private case class Bomb(location: IntervalVector, efficiency: java.lang.Double) {

    def explode(power: Map[String, Double], f: Map[String, Interval] => Interval, area: Area): (Bomb, Bomb) = {
      val splitComponent = location.getWidestComponent()
      val Seq(b1, b2) = location.split(ratios = Seq(1.0, 1.0), key = Some(splitComponent))
      val p1 = (power - splitComponent).map { case (k, v) => (k, (-v, v)) } + (splitComponent -> (-power(splitComponent), 0.0))
      val p2 = (power - splitComponent).map { case (k, v) => (k, (-v, v)) } + (splitComponent -> (0.0, power(splitComponent).doubleValue()))
      val shift_1 = GoRN.getContinuousUniformScala(p1)
      val shift_2 = GoRN.getContinuousUniformScala(p2)
      val selected_1 = area.keys.map(k => (k, shift_1(k)))
      val selected_2 = area.keys.map(k => (k, shift_2(k)))
      val moved_1 = b1.moveByScala(selected_1)
      val moved_2 = b2.moveByScala(selected_2)
      (Bomb(moved_1, moved_1.getPerformance(f)), Bomb(moved_2, moved_2.getPerformance(f)))
    }

  }

  private final class GenerateInitialBombsNode(override val nodeId: java.lang.Integer) extends GeneralNode[IntervalVector, Interval, IntervalVector](nodeId) {

    override def initialize(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {

      val maxBombs = state.getParameter[java.lang.Integer](maxBombsName)
      val bombs: Seq[Bomb] = (1 to maxBombs).map { _ =>
        val v: IntervalVector = area.mapValues { case (a, b) =>
          val p1 = GoRN.getContinuousUniform(a, b)
          val p2 = GoRN.getContinuousUniform(a, b)
          if (p1 <= p2) Interval(p1, p2)
          else Interval(p2, p1)
        }
        Bomb(v, v.getPerformance(f))
      }.sortBy(_.efficiency)

      state.setParameter(bombsName, bombs)

    }

    override def process(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {}

  }

  private final class PowerCalculationNode(override val nodeId: java.lang.Integer) extends GeneralNode[IntervalVector, Interval, IntervalVector](nodeId) {

    override def initialize(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {

      val rMax = state.getParameter[Map[String, java.lang.Double]](rMaxName)
      val maxBombs = state.getParameter[java.lang.Integer](maxBombsName)

      val maxPower = Range(0, maxBombs).map{ i =>
        val coeff = i / (maxBombs - 1.0)
        rMax.mapValues(coeff * _)
      }

      state.setParameter(maxPowerName, maxPower)

    }

    override def process(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {}

  }

  private final class ExplosionNode(override val nodeId: java.lang.Integer) extends GeneralNode[IntervalVector, Interval, IntervalVector](nodeId) {

    override def initialize(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = { }

    override def process(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {

      val bombs = state.getParameter[Seq[Bomb]](bombsName)
      val maxPower = state.getParameter[Seq[Map[String, Double]]](maxPowerName)

      val pieces = bombs.zip(maxPower)
        .map { case (b, p) => b.explode(p, f, area) }
        .foldLeft(Seq.empty[Bomb]) { case (seq, (b1, b2)) => b1 +: b2 +: seq }

      state.setParameter(bombsName, pieces)

    }

  }

  private final class RenewalNode(override val nodeId: java.lang.Integer) extends GeneralNode[IntervalVector, Interval, IntervalVector](nodeId) {

    override def initialize(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = { }

    override def process(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {

      val bombs = state.getParameter[Seq[Bomb]](bombsName)
      val maxBombs = state.getParameter[java.lang.Integer](maxBombsName)
      val newBombs = bombs.sortBy(_.efficiency).take(maxBombs)

      state.setParameter(bombsName, newBombs)

    }

  }

  private final class SetBestNode(override val nodeId: java.lang.Integer) extends GeneralNode[IntervalVector, Interval, IntervalVector](nodeId) {

    override def initialize(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = { }

    override def process(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {
      state.result = Some(state.getParameter[Seq[Bomb]](bombsName).head.location)
    }

  }

  def createExplosionSearch(maxBombs: java.lang.Integer, rMax: Map[String, java.lang.Double], maxTime: java.lang.Double): Algorithm[IntervalVector, Interval, IntervalVector] = {
    val ES_nodes = Seq(
      new SetParametersNode[IntervalVector, Interval, IntervalVector](nodeId = 0, parameters = Map(maxBombsName -> maxBombs, rMaxName -> rMax)),
      new GenerateInitialBombsNode(nodeId = 1),
      new PowerCalculationNode(nodeId = 2),
      new ExplosionNode(nodeId = 3),
      new RenewalNode(nodeId = 4),
      new TerminationViaMaxTime[IntervalVector, Interval, IntervalVector](nodeId = 5, maxTime),
      new SetBestNode(nodeId = 6)
    )

    val ES_transitionMatrix: Seq[(java.lang.Integer, Option[java.lang.Integer], java.lang.Integer)] = Seq(
      (0, None, 1),
      (1, None, 2),
      (2, None, 3),
      (3, None, 4),
      (4, None, 5),
      (5, Some(0), 3),
      (5, Some(1), 6)
    )

    new Algorithm[IntervalVector, Interval, IntervalVector](nodes = ES_nodes, transitionMatrix = ES_transitionMatrix)
  }

}
