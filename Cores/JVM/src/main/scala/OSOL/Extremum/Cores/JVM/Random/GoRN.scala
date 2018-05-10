package OSOL.Extremum.Cores.JVM.Random

import OSOL.Extremum.Cores.JVM.Random.Distributions._
import OSOL.Extremum.Cores.JVM.Random.Distributions.{ContinuousUniform, DiscreteUniform, Normal}

object GoRN
  extends DiscreteUniform
    with ContinuousUniform
    with Normal {

  private val core = new scala.util.Random()

  def resetCore(seed: java.lang.Long): Unit = core.setSeed(seed)

  override def getDiscreteUniform(min: java.lang.Integer, max: java.lang.Integer): java.lang.Integer = min + core.nextInt(max - min + 1)

  override def getContinuousUniform(min: java.lang.Double, max: java.lang.Double): java.lang.Double = min + core.nextDouble() * (max - min)

  override def getNormal(mu: java.lang.Double, sigma: java.lang.Double): java.lang.Double = {

    var x = getContinuousUniform(-1.0, 1.0)
    var y = getContinuousUniform(-1.0, 1.0)
    var s = x * x + y * y

    while (s > 1) {
      x = getContinuousUniform(-1.0, 1.0)
      y = getContinuousUniform(-1.0, 1.0)
      s = x * x + y * y
    }

    val z = x * math.sqrt(-2 * math.log(s) / s)
    mu + sigma * z

  }

  def getFromSeries[T](data: Seq[T], n: java.lang.Integer, withReturn: java.lang.Boolean): Seq[T] =
    withReturn match {
      case java.lang.Boolean.TRUE => Seq.fill(n)(getDiscreteUniform(0, data.size - 1)).map(x => data(x))
      case java.lang.Boolean.FALSE => data.map(x => (x, getContinuousUniform(0.0, 1.0))).sortBy(_._2).map(_._1).take(n)
    }

}