package OSOL.Extremum.Cores.JVM.Random.Distributions

trait ContinuousUniform {

  def getContinuousUniform(min: java.lang.Double, max: java.lang.Double): java.lang.Double

  final def getContinuousUniform(area: Map[String, (java.lang.Double, java.lang.Double)]): Map[String, java.lang.Double] =
    area.map { case (key, (min, max)) => (key, getContinuousUniform(min, max)) }

  def getContinuousUniformScala(min: Double, max: Double): Double =
    getContinuousUniform(min, max).doubleValue()

  final def getContinuousUniformScala(area: Map[String, (Double, Double)]): Map[String, Double] =
    area.map { case (key, (min, max)) => (key, getContinuousUniformScala(min, max)) }


}