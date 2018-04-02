package OSOL.Extremum.Core.Scala.Random.Distributions

trait DiscreteUniform {

  def getDiscreteUniform(min: Int, max: Int): Int

  final def getDiscreteUniform(area: Map[String, (Int, Int)]): Map[String, Int] =
    area.map { case (key, (min, max)) => (key, getDiscreteUniform(min, max)) }

}