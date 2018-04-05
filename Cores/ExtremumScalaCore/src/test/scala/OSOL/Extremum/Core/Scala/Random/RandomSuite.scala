package OSOL.Extremum.Core.Scala.Random

import org.scalatest.FunSuite

class RandomSuite extends FunSuite {

  val eps = 1e-2
  val N = 1e6.toInt
  val seed = 17091992L

  def getProbability[T](values: Seq[T], project: T => Int): Map[Int, Double] = {
    val valuesProjected = values.map(project)
    valuesProjected
      .distinct
      .map { value => (value, valuesProjected.count(_ == value).toDouble / valuesProjected.length) }
      .toMap
  }

  implicit class OverloadedMap[T](val v: Map[T, Double]) {
    def ~(that: OverloadedMap[T]): Double = {
      val keys = (this.v.keys ++ that.v.keys).toSeq.distinct
      keys
        .map { key =>
          val v1 = this.v.getOrElse(key, 0.0)
          val v2 = that.v.getOrElse(key, 0.0)
          math.abs(v1 - v2)
        }.sum / keys.length
    }
  }


  GoRN.resetCore(seed)

  test("Test \"getProbability\" function") {
    val initialValues = Seq(0.1, 0.2, 0.5, 2.1, 2.2, 3.4)
    val project =
      (x: Double) => {
        if (x <= 1.0) 0
        else {
          if (x <= 2.0) 1
          else {
            if (x <= 3.0) 2
            else 3
          }
        }
      }
    assert(getProbability(initialValues, project) == Map(0 -> 0.5, 2 -> 1.0 / 3.0, 3 -> 1.0 / 6.0))
  }

  test("Test \"~\" function") {
    val prob = Map(1 -> 1.0 / 7.0, 2 -> 3.0 / 7.0, 3 -> 2.0 / 7.0, 4 -> 1.0 / 7.0)
    val numOfDigits = math.round(1.0 / (0.1 * eps))
    val probRounded = prob.mapValues(value => math.round(numOfDigits * value).toDouble / numOfDigits)
    assert(prob ~ probRounded < eps)
  }

  test("Discrete Uniform") {
    val idealProb_x = Map(0 -> 0.5, 1 -> 0.5)
    val idealProb_y = Map(0 -> 1.0 / 3.0, 1 -> 1.0 / 3.0, 2 -> 1.0 / 3.0)

    val samples = (1 to N).map(_ => GoRN.getDiscreteUniform(Map("x" -> (0, 1), "y" -> (0, 2))))
    val calculatedProb_x = getProbability(samples.map(_("x")), (x: Int) => x)
    val calculatedProb_y = getProbability(samples.map(_("y")), (x: Int) => x)

    assert(idealProb_x ~ calculatedProb_x < eps)
    assert(idealProb_y ~ calculatedProb_y < eps)
  }

  test("Continuous Uniform") {
    val idealProb_x = (1 to 4).map((_, 0.25)).toMap
    val idealProb_y = (1 to 10).map((_, 0.1)).toMap

    val samples = (1 to N).map(_ => GoRN.getContinuousUniform(Map("x" -> (0.0, 4.0), "y" -> (0.0, 10.0))))
    val f = (x: Double) => math.ceil(x).toInt
    val calculatedProb_x = getProbability(samples.map(_("x")), f)
    val calculatedProb_y = getProbability(samples.map(_("y")), f)

    assert(idealProb_x ~ calculatedProb_x < eps)
    assert(idealProb_y ~ calculatedProb_y < eps)
  }

  test("Normal + Statistic") {
    val (mu_x, sigma_x) = (17.0, 7.0)
    val (mu_y, sigma_y) = (7.0, 17.0)

    val maxAttempts = 10

    val result = (1 to maxAttempts).foldLeft(false) { case (success, _) =>
      if (success) success
      else {
        val samples = (1 to 3 * N).map(_ => GoRN.getNormal(Map("x" -> (mu_x, sigma_x), "y" -> (mu_y, sigma_y))))
        val (muEst_x, sigmaEst_x) = (Statistics.getMean(samples.map(_ ("x"))), Statistics.getUnbiasedSigma(samples.map(_ ("x"))))
        val (muEst_y, sigmaEst_y) = (Statistics.getMean(samples.map(_ ("y"))), Statistics.getUnbiasedSigma(samples.map(_ ("y"))))

        val success_MuX = math.abs(mu_x - muEst_x) < eps
        val successSigmaX = math.abs(sigma_x - sigmaEst_x) < eps
        val success_MuY = math.abs(mu_y - muEst_y) < eps
        val successSigmaY = math.abs(sigma_y - sigmaEst_y) < eps

        success_MuX && successSigmaX && success_MuY && successSigmaY
      }
    }
    assert(result)
  }

  test("Get from Series") {
    val elements = Seq(1, 2, 3)

    val chosenWithReturn = (1 to N/100)
      .map(_ => GoRN.getFromSeries(elements, 5, withReturn = true))
      .foldLeft(Seq.empty[Int]) { case (seq, chosen) => seq ++ chosen }

    val chosenWithoutReturn = (1 to N/100)
      .map(_ => GoRN.getFromSeries(elements, 2, withReturn = false))
      .foldLeft(Seq.empty[Int]) { case (seq, chosen) => seq ++ chosen }

    assert(getProbability(chosenWithReturn, (x: Int) => x) ~ Map(1 -> 1.0/3.0, 2 -> 1.0/3.0, 3 -> 1.0/3.0) < eps)
    assert(getProbability(chosenWithoutReturn, (x: Int) => x) ~ Map(1 -> 1.0/3.0, 2 -> 1.0/3.0, 3 -> 1.0/3.0) < eps)

  }

}
