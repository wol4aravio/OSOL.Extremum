package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Optimization.Nodes.{GeneralNode, SetParametersNode, TerminationViaMaxTime}
import OSOL.Extremum.Core.Scala.Random.GoRN
import OSOL.Extremum.Core.Scala.Vectors.RealVector
import OSOL.Extremum.Core.Scala.Vectors.RealVector.Converters._

object RandomSearch {

  val currentPointName = "currentPoint"
  val currentPointEfficiencyName = "currentPointEfficiency"
  val radiusParameterName = "r"

  def generateRandomOnSphere(currentPoint: RealVector, radius: Double, area: Area): RealVector = {
    val normallyDistributed = GoRN.getNormal(area.mapValues(_ => (0.0, 1.0)))
    val r = math.sqrt(normallyDistributed.values.map(v => v * v).sum)
    (currentPoint + normallyDistributed * (GoRN.getContinuousUniform(-1.0, 1.0) / r)).constrain(area)
  }

  final class GenerateInitialPointNode(override val nodeId: Int) extends GeneralNode[RealVector, Double, RealVector](nodeId) {

    override def initialize(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = {
      val initialPoint: RealVector = GoRN.getContinuousUniform(area)
      state.setParameter(currentPointName, initialPoint)
      state.setParameter(currentPointEfficiencyName, initialPoint.getPerformance(f))
    }

    override def process(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = { }

  }

  final class SampleNewPointNode_FixedStep(override val nodeId: Int) extends GeneralNode[RealVector, Double, RealVector](nodeId) {

    override def initialize(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = { }

    override def process(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = {
      val currentPoint = state.getParameter[RealVector](currentPointName)
      val currentPointEfficiency = state.getParameter[Double](currentPointEfficiencyName)
      val r = state.getParameter[Double](radiusParameterName)

      val newPoint = generateRandomOnSphere(currentPoint, r, area)
      val newPointEfficiency = newPoint.getPerformance(f)

      if (newPointEfficiency < currentPointEfficiency) {
        state.setParameter(currentPointName, newPoint)
        state.setParameter(currentPointEfficiencyName, newPointEfficiency)
      }
    }

  }

  final class SetBestNode(override val nodeId: Int) extends GeneralNode[RealVector, Double, RealVector](nodeId) {

    override def initialize(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = { }

    override def process(f: Map[String, Double] => Double, area: Area, state: State[RealVector, Double, RealVector]): Unit = {
      state.result = Some(state.getParameter[RealVector](currentPointName))
    }

  }

  def createFixedStepRandomSearch(radius: Double, maxTime: Double): Algorithm[RealVector, Double, RealVector] = {
    val FixedStep_nodes = Seq(
      new SetParametersNode[RealVector, Double, RealVector](nodeId = 0, parameters = Map(radiusParameterName -> radius)),
      new GenerateInitialPointNode(nodeId = 1),
      new TerminationViaMaxTime[RealVector, Double, RealVector](nodeId = 2, maxTime),
      new SampleNewPointNode_FixedStep(nodeId = 3),
      new SetBestNode(nodeId = 4)
    )

    val FixedStep_transitionMatrix = Seq(
      (0, None, 1),
      (1, None, 2),
      (2, Some(0), 3),
      (2, Some(1), 4),
      (3, None, 2)
    )

    new Algorithm[RealVector, Double, RealVector](nodes = FixedStep_nodes, transitionMatrix = FixedStep_transitionMatrix)
  }

}
