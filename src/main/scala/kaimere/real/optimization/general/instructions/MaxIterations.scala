package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import spray.json._

case class MaxIterations(maxNumberOfIterations: Int, verbose: Boolean = false) extends GeneralInstruction {

  private var alreadyDone: Int = 0

  override def continue(algorithm: OptimizationAlgorithm): Boolean = {
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

object MaxIterations {

  implicit object MaxIterationsJsonFormat extends RootJsonFormat[MaxIterations] {
    def write(i: MaxIterations) =
      JsObject(
        "name" -> JsString("MaxIterations"),
        "maxNumberOfIterations" -> JsNumber(i.maxNumberOfIterations),
        "verbose" -> JsBoolean(i.verbose))

    def read(json: JsValue): MaxIterations =
      json.asJsObject.getFields("name", "maxNumberOfIterations", "verbose") match {
        case Seq(JsString(name), JsNumber(maxNumberOfIterations), JsBoolean(verbose)) =>
          if (name != "MaxIterations") throw DeserializationException("MaxIterations expected")
          else MaxIterations(maxNumberOfIterations.toInt, verbose)
        case _ => throw DeserializationException("MaxIterations expected")
      }
  }

}