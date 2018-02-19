package kaimere.real.optimization.general.initializers
import kaimere.real.objects.RealVector
import kaimere.real.optimization.general.{OptimizationAlgorithm, State}
import kaimere.tools.etc._

case class ExactInitializer(defaultValue: Double, keyValuePair: (String, Double)*) extends Initializer {

  override def generateState(algorithm: OptimizationAlgorithm): State =
    Vector(algorithm.area.map { case (key, _) => (key, keyValuePair.toMap.getOrElse(key, defaultValue)) } |> RealVector.apply) |> State.apply

}