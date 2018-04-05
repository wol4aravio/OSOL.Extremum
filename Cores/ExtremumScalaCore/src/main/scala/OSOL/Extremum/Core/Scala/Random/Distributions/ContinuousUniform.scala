package OSOL.Extremum.Core.Scala.Random.Distributions

/** Trait for object that supports continuous uniform distribution  */
trait ContinuousUniform {

  /** Generate random variable uniformly distributed in interval `[min; max]`
    *
    * @param min minimum possible value
    * @param max maximum possible value
    * @return random variable
    */
  def getContinuousUniform(min: Double, max: Double): Double

  /** Vector form of [[OSOL.Extremum.Core.Scala.Random.Distributions.ContinuousUniform#getContinuousUniform(Double,Double) getContinuousUniform]] */
  final def getContinuousUniform(area: Map[String, (Double, Double)]): Map[String, Double] =
    area.map { case (key, (min, max)) => (key, getContinuousUniform(min, max)) }

}