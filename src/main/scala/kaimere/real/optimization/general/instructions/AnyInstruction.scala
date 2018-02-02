package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import spray.json._

case class AnyInstruction(instructions: Seq[GeneralInstruction]) extends GeneralInstruction {

  override def continue(algorithm: OptimizationAlgorithm): Boolean =
    instructions.map(_.continue(algorithm)).reduce(_ || _)

  override def reset(): Unit = instructions.foreach(_.reset())

}

object AnyInstruction {

  implicit object AnyInstructionJsonFormat extends RootJsonFormat[AnyInstruction] {
    def write(i: AnyInstruction) =
      JsObject(
        "name" -> JsString("All"),
        "instructions" -> JsArray(i.instructions.map(GeneralInstruction.toJson).toVector))

    def read(json: JsValue): AnyInstruction =
      json.asJsObject.getFields("name", "instructions") match {
        case Seq(JsString(name), JsArray(instructions)) =>
          if (name != "AnyInstruction") throw DeserializationException("AnyInstruction expected")
          else AnyInstruction(instructions.map(GeneralInstruction.fromJson))
        case _ => throw DeserializationException("AnyInstruction expected")
      }
  }

}