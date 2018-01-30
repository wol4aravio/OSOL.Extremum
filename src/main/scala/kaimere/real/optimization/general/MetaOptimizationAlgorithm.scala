package kaimere.real.optimization.general

import kaimere.real.objects
import kaimere.real.objects.{Function, RealVector}
import kaimere.real.optimization.general.MetaOptimizationAlgorithm.MOA_State
import kaimere.real.optimization.general.OptimizationAlgorithm.Area
import kaimere.tools.random.GoRN
import kaimere.tools.etc._

case class MetaOptimizationAlgorithm(algorithms: Seq[OptimizationAlgorithm],
                                     targetVars: Seq[Option[Set[String]]],
                                     instructions: Seq[Instruction]) extends OptimizationAlgorithm {

  protected var algorithmArea: Seq[OptimizationAlgorithm.Area] = Seq.empty

  override def initializeRandomState(): State = {
    val v = GoRN.getContinuousUniform(area)
    MOA_State(v)
  }

  override def initializeFromGivenState(state: Vector[Map[String, Double]]): State = {
    val realVectors = state.map(x => x.map { case (key, value) => (key, value) }).map(RealVector.fromMap)
    realVectors.minBy(f(_)) |> MOA_State
  }

  override def iterate(): Unit = ???

  override def initialize(f: objects.Function, area: Area, state: Option[Vector[Map[String, Double]]]): Unit = {
    super.initialize(f, area, state)
    algorithmArea = targetVars.map {
      case Some(vars) => vars.map(key => (key, area(key))).toMap[String, (Double, Double)]
      case None => area
    }

  }

  override def work(instruction: Instruction): RealVector = {
    val MOA_State(initialSeed) = currentState
    algorithms.indices.foldLeft(initialSeed) { case (seed, id) =>
      println(s"Processing ${id + 1}/${algorithms.size}")
        val tempArea = seed.vals.map { case (key, v) => (key, (v, v)) } ++ algorithmArea(id)
        algorithms(id).initialize(f, tempArea, state = Some(Vector(seed.vals)))
        val tempResult = algorithms(id).work(instructions(id))
        currentState = MOA_State(tempResult)
        tempResult
    }
  }


}

object MetaOptimizationAlgorithm {

  case class MOA_State(v: RealVector) extends State {

    def apply(v: RealVector): MOA_State = MOA_State(v)

    override def toVectors(): Vector[RealVector] = Vector(v)

    override def getBestBy(f: Function): (RealVector, Double) = (v, f(v))

  }

}