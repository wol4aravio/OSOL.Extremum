package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import spray.json._

case class TargetValue(targetValue: Double, maxError: Double = 0.01, verbose: Boolean = false) extends GeneralInstruction {

  override def continue(algorithm: OptimizationAlgorithm): Boolean = {
    val currentBestValue = algorithm.currentState.getBestBy(algorithm.f)._2
    val delta = (currentBestValue - targetValue) / math.max(math.abs(targetValue), 1e-5)
    if (verbose) println(s"Current delta: ${truncate(100.0 * delta)}%")
    delta >= maxError
  }

  override def reset(): Unit = { }

}

object TargetValue {

  implicit object TargetValueJsonFormat extends RootJsonFormat[TargetValue] {
    def write(i: TargetValue) =
      JsObject(
        "name" -> JsString("TargetValue"),
        "targetValue" -> JsNumber(i.targetValue),
        "maxError" -> JsNumber(i.maxError),
        "verbose" -> JsBoolean(i.verbose))

    def read(json: JsValue): TargetValue =
      json.asJsObject.getFields("name", "targetValue", "maxError", "verbose") match {
        case Seq(JsString(name), JsNumber(targetValue), JsNumber(maxError), JsBoolean(verbose)) =>
          if (name != "TargetValue") throw DeserializationException("TargetValue expected")
          else TargetValue(targetValue.toDouble, maxError.toDouble, verbose)
        case _ => throw DeserializationException("TargetValue expected")
      }
  }

}