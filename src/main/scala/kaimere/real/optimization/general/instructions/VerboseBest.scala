package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import spray.json._

case class VerboseBest(mainInstruction: GeneralInstruction) extends GeneralInstruction {

  override def continue(algorithm: OptimizationAlgorithm): Boolean = {
    val continueOrNot = mainInstruction.continue(algorithm)
    println(algorithm.currentState.getBestBy(algorithm.f)._2)
    continueOrNot
  }

  override def reset(): Unit = mainInstruction.reset()

}

object VerboseBest {

  implicit object VerboseBestJsonFormat extends RootJsonFormat[VerboseBest] {
    def write(i: VerboseBest) =
      JsObject(
        "name" -> JsString("MaxTime"),
        "mainInstruction" -> GeneralInstruction.toJson(i.mainInstruction))

    def read(json: JsValue): VerboseBest =
      json.asJsObject.getFields("name", "mainInstruction") match {
        case Seq(JsString(name), mainInstruction) =>
          if (name != "VerboseBest") throw DeserializationException("VerboseBest expected")
          else VerboseBest(GeneralInstruction.fromJson(mainInstruction))
        case _ => throw DeserializationException("VerboseBest expected")
      }
  }

}