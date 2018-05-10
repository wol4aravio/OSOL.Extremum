package OSOL.Extremum.Cores.JVM.Random

object Statistics {

  def sampleMoment(data: Traversable[Double], n: Int): Double =
    data.map(x => math.pow(x, n)).sum / data.size

  def getMean(data: Traversable[Double]): Double = sampleMoment(data, 1)

  def centralMoment(data: Traversable[Double], n: Int): Double = {
    val average = getMean(data)
    data.map(x => math.pow(x - average, n)).sum / data.size
  }

  def getUnbiasedSigma(data: Traversable[Double]): Double = math.sqrt((data.size / (data.size - 1.0)) * centralMoment(data, 2))

}
