package kaimere.real.optimization.basic

trait Instruction {

  def continue(): Boolean
  def reset(): Unit

}

object Instruction {

  case class MaxIterations(maxNumberOfIterations: Int) extends Instruction {

    private var alreadyDone: Int = 0

    override def continue(): Boolean = {
      alreadyDone += 1
      return alreadyDone <= maxNumberOfIterations
    }

    override def reset(): Unit = {
      alreadyDone = 0
    }

  }
  case class MaxTime(maxSeconds: Double) extends Instruction {

    private var startTime: Long = System.nanoTime()

    override def continue(): Boolean = {
      return 1e-9 * (System.nanoTime() - startTime) <= maxSeconds
    }

    override def reset(): Unit = {
      startTime = System.nanoTime()
    }

  }

}