package kaimere.real.optimization.general.initializers

import kaimere.real.optimization.general.OptimizationAlgorithm

trait Initializer {

  def generateState(algorithm: OptimizationAlgorithm): Vector[Map[String, Double]]

}
