package OSOL.Extremum.Cores.JVM.Random.Distributions

trait Normal {

  def getNormal(mu: java.lang.Double, sigma: java.lang.Double): java.lang.Double

  final def getNormal(area: Map[String, (java.lang.Double, java.lang.Double)]): Map[String, java.lang.Double] =
    area.map { case (key, (mu, sigma)) => (key, getNormal(mu, sigma)) }

  def getNormalScala(mu: Double, sigma: Double): Double =
    getNormal(mu, sigma)

  final def getNormalScala(area: Map[String, (Double, Double)]): Map[String, Double] =
    area.map { case (key, (mu, sigma)) => (key, getNormalScala(mu, sigma)) }

}