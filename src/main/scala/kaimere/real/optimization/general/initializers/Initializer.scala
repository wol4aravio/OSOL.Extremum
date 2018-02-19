package kaimere.real.optimization.general.initializers

import kaimere.real.optimization.general.{OptimizationAlgorithm, State}

trait Initializer {

  def generateState(algorithm: OptimizationAlgorithm): State

}
