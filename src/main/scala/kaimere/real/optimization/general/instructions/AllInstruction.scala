package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import spray.json._

case class AllInstruction(instructions: Instruction*) extends Instruction {

  override def continue(algorithm: OptimizationAlgorithm): Boolean =
    instructions.map(_.continue(algorithm)).reduce(_ && _)

  override def reset(): Unit = instructions.foreach(_.reset())

}

object AllInstruction {

  def apply(csv: String): AllInstruction = {
    val name = csv.split(",").head
    val instructions = csv.split(",").tail.mkString(",").split("&")
    name match {
      case "AllInstruction" => AllInstruction(instructions.map(Instruction.fromCsv):_*)
      case _ => throw DeserializationException("AllInstruction expected")
    }
  }

  implicit object AllInstructionJsonFormat extends RootJsonFormat[AllInstruction] {
    def write(i: AllInstruction) =
      JsObject(
        "name" -> JsString("AllInstruction"),
        "instructions" -> JsArray(i.instructions.map(Instruction.toJson).toVector))

    def read(json: JsValue): AllInstruction =
      json.asJsObject.getFields("name", "instructions") match {
        case Seq(JsString(name), JsArray(instructions)) =>
          if (name != "AllInstruction") throw DeserializationException("AllInstruction expected")
          else AllInstruction(instructions.map(Instruction.fromJson):_*)
        case _ => throw DeserializationException("AllInstruction expected")
      }
  }

}
