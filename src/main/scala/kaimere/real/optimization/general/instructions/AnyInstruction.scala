package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import spray.json._

case class AnyInstruction(instructions: Instruction*) extends Instruction {

  override def continue(algorithm: OptimizationAlgorithm): Boolean =
    instructions.map(_.continue(algorithm)).reduce(_ || _)

  override def reset(): Unit = instructions.foreach(_.reset())

}

object AnyInstruction {

  def apply(csv: String): AnyInstruction = {
    val name = csv.split(",").head
    val instructions = csv.split(",").tail.mkString(",").split("\\|")
    name match {
      case "AnyInstruction" => AnyInstruction(instructions.map(Instruction.fromCsv):_*)
      case _ => throw DeserializationException("AnyInstruction expected")
    }
  }

  implicit object AnyInstructionJsonFormat extends RootJsonFormat[AnyInstruction] {
    def write(i: AnyInstruction) =
      JsObject(
        "name" -> JsString("AnyInstruction"),
        "instructions" -> JsArray(i.instructions.map(Instruction.toJson).toVector))

    def read(json: JsValue): AnyInstruction =
      json.asJsObject.getFields("name", "instructions") match {
        case Seq(JsString(name), JsArray(instructions)) =>
          if (name != "AnyInstruction") throw DeserializationException("AnyInstruction expected")
          else AnyInstruction(instructions.map(Instruction.fromJson):_*)
        case _ => throw DeserializationException("AnyInstruction expected")
      }
  }

}