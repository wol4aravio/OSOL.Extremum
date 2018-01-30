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
      return alreadyDone <= maxNumberOfIterations
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
      return alreadyPassed <= maxSeconds
    }

    override def reset(): Unit = {
      startTime = System.nanoTime()
    }

  }

  case class Verbose(algorithm: OptimizationAlgorithm, mainInstruction: Instruction) extends Instruction(algorithm) {

    override def continue(): Boolean = {
      println(algorithm.currentState.getBestBy(algorithm.f)._2)
      mainInstruction.continue()
    }

    override def reset(): Unit = mainInstruction.reset()

  }

}