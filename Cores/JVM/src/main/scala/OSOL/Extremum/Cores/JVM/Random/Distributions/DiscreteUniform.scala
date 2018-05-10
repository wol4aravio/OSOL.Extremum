package OSOL.Extremum.Cores.JVM.Random.Distributions

trait DiscreteUniform {

  def getDiscreteUniform(min: java.lang.Integer, max: java.lang.Integer): java.lang.Integer

  final def getDiscreteUniform(area: Map[String, (java.lang.Integer, java.lang.Integer)]): Map[String, java.lang.Integer] =
    area.map { case (key, (min, max)) => (key, getDiscreteUniform(min, max)) }

  def getDiscreteUniformScala(min: Int, max: Int): Int =
    getDiscreteUniform(min, max).intValue()

  final def getDiscreteUniformScala(area: Map[String, (Int, Int)]): Map[String, Int] =
    area.map { case (key, (min, max)) => (key, getDiscreteUniformScala(min, max)) }

}