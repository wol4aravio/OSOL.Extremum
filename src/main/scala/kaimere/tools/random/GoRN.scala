package kaimere.tools.random

import kaimere.tools.random.distributions._

object GoRN
  extends DiscreteUniform
    with ContinuousUniform
    with Normal {

  private val core = new scala.util.Random()

  def resetCore(seed: Long): Unit = core.setSeed(seed)

  override def getDiscreteUniform(min: Int, max: Int): Int = min + core.nextInt(max - min + 1)

  override def getContinuousUniform(min: Double, max: Double): Double = min + core.nextDouble() * (max - min)

  override def getNormal(mu: Double, sigma: Double): Double = {

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

  def getFromSeries[T](data: Seq[T], n: Int, withReturn: Boolean): Seq[T] =
    withReturn match {
      case true => Seq.fill(n)(getDiscreteUniform(0, data.size - 1)).map(x => data(x))
      case false => data.map(x => (x, getContinuousUniform(0.0, 1.0))).sortBy(_._2).map(_._1).take(n)
    }

}