package kaimere.tools.random

import org.scalatest.FunSuite

class GoRN_Suite extends FunSuite {

  val eps = 1e-2
  val N = 1e6.toInt
  val seed = 17091992L

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

    val samples = (1 to 3 * N).map(_ => GoRN.getNormal(Map("x" -> (mu_x, sigma_x), "y" -> (mu_y, sigma_y))))
    val (muEst_x, sigmaEst_x) = (Statistics.getAverage(samples.map(_("x"))), Statistics.getUnbiasedSigma(samples.map(_("x"))))
    val (muEst_y, sigmaEst_y) = (Statistics.getAverage(samples.map(_("y"))), Statistics.getUnbiasedSigma(samples.map(_("y"))))

    assert(math.abs(mu_x - muEst_x) < eps)
    assert(math.abs(sigma_x - sigmaEst_x) < eps)

    assert(math.abs(mu_y - muEst_y) < eps)
    assert(math.abs(sigma_y - sigmaEst_y) < eps)
  }
}