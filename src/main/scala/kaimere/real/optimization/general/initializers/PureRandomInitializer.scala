package kaimere.real.optimization.general.initializers
import kaimere.real.objects.RealVector
import kaimere.real.optimization.general.{OptimizationAlgorithm, State}
import kaimere.tools.random.GoRN
import kaimere.tools.etc._

case class PureRandomInitializer(capacity: Int) extends Initializer {

  override def generateState(algorithm: OptimizationAlgorithm): State =
    (1 to capacity).map(_ => GoRN.getContinuousUniform(algorithm.area) |> RealVector.apply ).toVector |> State.apply

}
