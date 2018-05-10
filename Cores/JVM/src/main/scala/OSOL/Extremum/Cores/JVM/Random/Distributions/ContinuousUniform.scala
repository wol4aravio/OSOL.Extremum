package OSOL.Extremum.Cores.JVM.Random.Distributions

trait ContinuousUniform {

  def getContinuousUniform(min: Double, max: Double): Double

  final def getContinuousUniform(area: Map[String, (Double, Double)]): Map[String, Double] =
    area.map { case (key, (min, max)) => (key, getContinuousUniform(min, max)) }

}