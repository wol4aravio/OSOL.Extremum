package OSOL.Extremum.Core.Scala.Random.Distributions

/** Trait for object that supports normal distribution  */
trait Normal {

  /** Generate random variable normally distributed with parameters mu & sigma
    *
    * @param mu mean
    * @param sigma deviation parameter
    * @return random variable
    */
  def getNormal(mu: Double, sigma: Double): Double

  /** Vector form of [[OSOL.Extremum.Core.Scala.Random.Distributions.Normal#getNormal(Double,Double) getNormal]] */
  final def getNormal(area: Map[String, (Double, Double)]): Map[String, Double] =
    area.map { case (key, (mu, sigma)) => (key, getNormal(mu, sigma)) }

}