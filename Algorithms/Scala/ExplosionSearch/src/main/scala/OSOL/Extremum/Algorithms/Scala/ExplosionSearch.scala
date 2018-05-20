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

      val maxPower = Range(0, maxBombs).map{i =>
        val coeff = (i - 1.0) / (maxBombs - 1.0)
        rMax.mapValues(coeff * _)
      }

      state.setParameter(maxPowerName, maxPower)

    }

    override def process(f: Map[String, Interval] => Interval, area: Area, state: State[IntervalVector, Interval, IntervalVector]): Unit = {}

  }



}
