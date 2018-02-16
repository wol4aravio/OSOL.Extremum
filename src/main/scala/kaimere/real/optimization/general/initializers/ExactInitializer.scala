package kaimere.real.optimization.general.initializers
import kaimere.real.optimization.general.OptimizationAlgorithm
import kaimere.tools.random.GoRN

case class ExactInitializer(defaultValue: Double, keyValuePair: (String, Double)*) extends Initializer {

  override def generateState(algorithm: OptimizationAlgorithm): Vector[Map[String, Double]] =
    Vector(algorithm.area.map { case (key, _) => (key, keyValuePair.toMap.getOrElse(key, defaultValue)) })

}