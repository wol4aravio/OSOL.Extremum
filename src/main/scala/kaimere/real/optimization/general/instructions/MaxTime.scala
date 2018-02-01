package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import spray.json._

case class MaxTime(maxSeconds: Double, verbose: Boolean = false) extends GeneralInstruction {

  private var startTime: Long = System.nanoTime()

  override def continue(algorithm: OptimizationAlgorithm): Boolean = {
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

object MaxTime {

  implicit object MaxTimeJsonFormat extends RootJsonFormat[MaxTime] {
    def write(i: MaxTime) =
      JsObject(
        "name" -> JsString("MaxTime"),
        "maxSeconds" -> JsNumber(i.maxSeconds),
        "verbose" -> JsBoolean(i.verbose))

    def read(json: JsValue): MaxTime =
      json.asJsObject.getFields("name", "maxSeconds", "verbose") match {
        case Seq(JsString(name), JsNumber(maxSeconds), JsBoolean(verbose)) =>
          if (name != "MaxTime") throw DeserializationException("MaxTime expected")
          else MaxTime(maxSeconds.toDouble, verbose)
        case _ => throw DeserializationException("MaxTime expected")
      }
  }

}