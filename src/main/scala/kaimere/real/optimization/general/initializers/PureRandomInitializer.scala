package kaimere.real.optimization.general.initializers
import kaimere.real.objects.RealVector
import kaimere.real.optimization.general.{OptimizationAlgorithm, State}
import kaimere.real.optimization.metaheuristic._
import kaimere.tools.random.GoRN
import kaimere.tools.etc._

case class PureRandomInitializer() extends Initializer {

  override def generateState(algorithm: OptimizationAlgorithm): State = {
    val capacity = algorithm match {
      case cso: CatSwarmOptimization => cso.numberOfCats
      case es: ExplosionSearch => es.numberOfBombs
      case hs: HarmonySearch => hs.numberOfHarmonics
      case _ => 1
    }
    (1 to capacity).map(_ => GoRN.getContinuousUniform(algorithm.area) |> RealVector.apply).toVector |> State.apply
  }
}
