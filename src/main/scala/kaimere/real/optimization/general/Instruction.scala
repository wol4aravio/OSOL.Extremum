package kaimere.real.optimization.general

import java.text.DecimalFormat

abstract class Instruction(algorithm: OptimizationAlgorithm) {

  def continue(): Boolean
  def reset(): Unit

}

object Instruction {

  def truncate(d: Double): String = new DecimalFormat("#.##").format(d)

  case class MaxIterations(maxNumberOfIterations: Int, verbose: Boolean = false) extends Instruction(null) {

    private var alreadyDone: Int = 0

    override def continue(): Boolean = {
      alreadyDone += 1
      if (verbose) {
        val progress = 100.0 * (alreadyDone - 1) / maxNumberOfIterations
        println(s"Current progress: ${truncate(progress)}%")
      }
      alreadyDone <= maxNumberOfIterations
    }

    override def reset(): Unit = {
      alreadyDone = 0
    }

  }

  case class MaxTime(maxSeconds: Double, verbose: Boolean = false) extends Instruction(null) {

    private var startTime: Long = System.nanoTime()

    override def continue(): Boolean = {
      val alreadyPassed = 1e-9 * (System.nanoTime() - startTime)
      if (verbose) {
        val progress = 100.0 * alreadyPassed / maxSeconds
        println(s"Current progress: ${truncate(progress)}%")
      }
      alreadyPassed <= maxSeconds
    }

    override def reset(): Unit = {
      startTime = System.nanoTime()
    }

  }

  case class TargetValue(algorithm: OptimizationAlgorithm, targetValue: Double, maxError: Double = 0.01, verbose: Boolean = false) extends Instruction(algorithm) {

    override def continue(): Boolean = {
      val currentBestValue = algorithm.currentState.getBestBy(algorithm.f)._2
      val delta = (currentBestValue - targetValue) / targetValue
      if (verbose) println(s"Current delta: ${truncate(100.0 * delta)}%")
      delta < maxError
    }

    override def reset(): Unit = { }

  }

  case class VerboseBest(algorithm: OptimizationAlgorithm, mainInstruction: Instruction) extends Instruction(algorithm) {

    override def continue(): Boolean = {
      val continueOrNot = mainInstruction.continue()
      println(algorithm.currentState.getBestBy(algorithm.f)._2)
      continueOrNot
    }

    override def reset(): Unit = mainInstruction.reset()

  }

}