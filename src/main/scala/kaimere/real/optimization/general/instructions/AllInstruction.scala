package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import spray.json._

case class AllInstruction(instructions: Seq[GeneralInstruction]) extends GeneralInstruction {

  override def continue(algorithm: OptimizationAlgorithm): Boolean =
    instructions.map(_.continue(algorithm)).reduce(_ && _)

  override def reset(): Unit = instructions.foreach(_.reset())

}

object AllInstruction {

  implicit object AllInstructionJsonFormat extends RootJsonFormat[AllInstruction] {
    def write(i: AllInstruction) =
      JsObject(
        "name" -> JsString("All"),
        "instructions" -> JsArray(i.instructions.map(GeneralInstruction.toJson).toVector))

    def read(json: JsValue): AllInstruction =
      json.asJsObject.getFields("name", "instructions") match {
        case Seq(JsString(name), JsArray(instructions)) =>
          if (name != "AllInstruction") throw DeserializationException("AllInstruction expected")
          else AllInstruction(instructions.map(GeneralInstruction.fromJson))
        case _ => throw DeserializationException("AllInstruction expected")
      }
  }

}
