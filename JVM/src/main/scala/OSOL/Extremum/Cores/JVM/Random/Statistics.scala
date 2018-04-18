package OSOL.Extremum.Cores.JVM.Random

/** Object that is used to calculate statistics of sequences */
object Statistics {

  /** Calculate sample moment from number sequence
    *
    * @param data input number sequence
    * @param n moment degree
    * @return sample moment
    */
  def sampleMoment(data: Traversable[Double], n: Int): Double =
    data.map(x => math.pow(x, n)).sum / data.size

  /** Ordinary sample mean
    *
    * @param data input number sequence
    * @return sample mean
    */
  def getMean(data: Traversable[Double]): Double = sampleMoment(data, 1)

  /** Calculate central sample moment from number sequence
    *
    * @param data input number sequence
    * @param n moment degree
    * @return central sample moment
    */
  def centralMoment(data: Traversable[Double], n: Int): Double = {
    val average = getMean(data)
    data.map(x => math.pow(x - average, n)).sum / data.size
  }

  /** Calculation of unbiased sigma
    *
    * @param data input number sequence
    * @return unbiased sigma
    */
  def getUnbiasedSigma(data: Traversable[Double]): Double = math.sqrt((data.size / (data.size - 1.0)) * centralMoment(data, 2))

}
