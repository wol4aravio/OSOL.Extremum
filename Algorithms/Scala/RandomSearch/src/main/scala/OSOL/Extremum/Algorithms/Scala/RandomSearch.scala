package OSOL.Extremum.Algorithms.Scala

import OSOL.Extremum.Cores.JVM.Optimization._
import OSOL.Extremum.Cores.JVM.Optimization.Nodes.{GeneralNode, SetParametersNode, TerminationViaMaxTime}
import OSOL.Extremum.Cores.JVM.Random.GoRN
import OSOL.Extremum.Cores.JVM.Vectors.RealVector
import OSOL.Extremum.Cores.JVM.Vectors.RealVector.Converters._

object RandomSearch {

  private val currentPointName = "currentPoint"
  private val currentPointEfficiencyName = "currentPointEfficiency"
  private val radiusParameterName = "r"

  private def generateRandomInSphere(currentPoint: RealVector, radius: Double, area: Area): RealVector = {
    val normallyDistributed = GoRN.getNormal(area.mapValues(_ => (0.0, 1.0)))
    val r = math.sqrt(normallyDistributed.values.map(v => v * v).sum)
    (currentPoint + normallyDistributed * (GoRN.getContinuousUniform(-1.0, 1.0) / r)).constrain(area)
  }

  private final class GenerateInitialPointNode(override val nodeId: java.lang.Integer) extends GeneralNode[RealVector, java.lang.Double, RealVector](nodeId) {

    override def initialize(f: Map[String, java.lang.Double] => java.lang.Double, area: Area, state: State[RealVector, java.lang.Double, RealVector]): Unit = {
      val initialPoint: RealVector = GoRN.getContinuousUniform(area)
      state.setParameter(currentPointName, initialPoint)
      state.setParameter(currentPointEfficiencyName, initialPoint.getPerformance(f))
    }

    override def process(f: Map[String, java.lang.Double] => java.lang.Double, area: Area, state: State[RealVector, java.lang.Double, RealVector]): Unit = { }

  }

  private final class SampleNewPointNode_FixedStep(override val nodeId: java.lang.Integer) extends GeneralNode[RealVector, java.lang.Double, RealVector](nodeId) {

    override def initialize(f: Map[String, java.lang.Double] => java.lang.Double, area: Area, state: State[RealVector, java.lang.Double, RealVector]): Unit = { }

    override def process(f: Map[String, java.lang.Double] => java.lang.Double, area: Area, state: State[RealVector, java.lang.Double, RealVector]): Unit = {
      val currentPoint = state.getParameter[RealVector](currentPointName)
      val currentPointEfficiency = state.getParameter[Double](currentPointEfficiencyName)
      val r = state.getParameter[Double](radiusParameterName)

      val newPoint = generateRandomInSphere(currentPoint, r, area)
      val newPointEfficiency = newPoint.getPerformance(f)

      if (newPointEfficiency < currentPointEfficiency) {
        state.setParameter(currentPointName, newPoint)
        state.setParameter(currentPointEfficiencyName, newPointEfficiency)
      }
    }

  }

  private final class SetBestNode(override val nodeId: java.lang.Integer) extends GeneralNode[RealVector, java.lang.Double, RealVector](nodeId) {

    override def initialize(f: Map[String, java.lang.Double] => java.lang.Double, area: Area, state: State[RealVector, java.lang.Double, RealVector]): Unit = { }

    override def process(f: Map[String, java.lang.Double] => java.lang.Double, area: Area, state: State[RealVector, java.lang.Double, RealVector]): Unit = {
      state.result = Some(state.getParameter[RealVector](currentPointName))
    }

  }

  def createFixedStepRandomSearch(radius: java.lang.Double, maxTime: java.lang.Double): Algorithm[RealVector, java.lang.Double, RealVector] = {
    val FixedStep_nodes = Seq(
      new SetParametersNode[RealVector, java.lang.Double, RealVector](nodeId = 0, parameters = Map(radiusParameterName -> radius)),
      new GenerateInitialPointNode(nodeId = 1),
      new TerminationViaMaxTime[RealVector, java.lang.Double, RealVector](nodeId = 2, maxTime),
      new SampleNewPointNode_FixedStep(nodeId = 3),
      new SetBestNode(nodeId = 4)
    )

    val FixedStep_transitionMatrix: Seq[(java.lang.Integer, Option[java.lang.Integer], java.lang.Integer)] = Seq(
      (0, None, 1),
      (1, None, 2),
      (2, Some(0), 3),
      (2, Some(1), 4),
      (3, None, 2)
    )

    new Algorithm[RealVector, java.lang.Double, RealVector](nodes = FixedStep_nodes, transitionMatrix = FixedStep_transitionMatrix)
  }

}
