package kaimere.real.optimization.general.initializers
import kaimere.real.optimization.general.OptimizationAlgorithm
import kaimere.tools.random.GoRN

case class PureRandomInitializer(capacity: Int) extends Initializer {

  override def generateState(algorithm: OptimizationAlgorithm): Vector[Map[String, Double]] =
    (1 to capacity).map(_ => GoRN.getContinuousUniform(algorithm.area)).toVector

}
