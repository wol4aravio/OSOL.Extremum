package OSOL.Extremum.Cores.JVM.Random.Distributions

/** Trait for object that supports discrete uniform distribution  */
trait DiscreteUniform {

  /** Generate random variable uniformly distributed in interval `[min; max]`
    *
    * @param min minimum possible value
    * @param max maximum possible value
    * @return random variable
    */
  def getDiscreteUniform(min: Int, max: Int): Int

  /** Vector form of [[OSOL.Extremum.Cores.JVM.Random.Distributions.DiscreteUniform#getDiscreteUniform(Integer,Integer) getDiscreteUniform]] */
  final def getDiscreteUniform(area: Map[String, (Int, Int)]): Map[String, Int] =
    area.map { case (key, (min, max)) => (key, getDiscreteUniform(min, max)) }

}