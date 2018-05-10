package OSOL.Extremum.Cores.JVM.Random

object Statistics {

  def sampleMoment(data: Traversable[java.lang.Double], n: java.lang.Integer): java.lang.Double =
    data.map(x => math.pow(x, n.doubleValue())).sum / data.size

  def getMean(data: Traversable[java.lang.Double]): java.lang.Double = sampleMoment(data, 1)

  def centralMoment(data: Traversable[java.lang.Double], n: java.lang.Integer): java.lang.Double = {
    val average = getMean(data)
    data.map(x => math.pow(x - average, n.doubleValue())).sum / data.size
  }

  def getUnbiasedSigma(data: Traversable[java.lang.Double]): java.lang.Double = math.sqrt((data.size / (data.size - 1.0)) * centralMoment(data, 2))

  def sampleMomentScala(data: Traversable[Double], n: Int): Double =
    sampleMoment(data.map(new java.lang.Double(_)), new java.lang.Integer(n))

  def getMeanScala(data: Traversable[Double]): Double = getMean(data.map(new java.lang.Double(_)))

  def centralMomentScala(data: Traversable[Double], n: Int): Double =
    centralMoment(data.map(new java.lang.Double(_)), new java.lang.Integer(1))

  def getUnbiasedSigmaScala(data: Traversable[Double]): Double =
    getUnbiasedSigma(data.map(new java.lang.Double(_)))

}
