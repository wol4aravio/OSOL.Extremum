package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import spray.json._

case class VerboseBest(mainInstruction: Instruction) extends Instruction {

  override def continue(algorithm: OptimizationAlgorithm): Boolean = {
    val continueOrNot = mainInstruction.continue(algorithm)
    println(algorithm.currentState.getBestBy(algorithm.f)._2)
    continueOrNot
  }

  override def reset(): Unit = mainInstruction.reset()

}

object VerboseBest {

  def apply(csv: String): VerboseBest = {
    val name = csv.split(",").head
    val instruction = csv.split(",").tail
    name match {
      case "VerboseBest" => VerboseBest(Instruction.fromCsv(instruction.mkString(",")))
      case _ => throw DeserializationException("VerboseBest expected")
    }
  }

  implicit object VerboseBestJsonFormat extends RootJsonFormat[VerboseBest] {
    def write(i: VerboseBest) =
      JsObject(
        "name" -> JsString("VerboseBest"),
        "mainInstruction" -> Instruction.toJson(i.mainInstruction))

    def read(json: JsValue): VerboseBest =
      json.asJsObject.getFields("name", "mainInstruction") match {
        case Seq(JsString(name), mainInstruction) =>
          if (name != "VerboseBest") throw DeserializationException("VerboseBest expected")
          else VerboseBest(Instruction.fromJson(mainInstruction))
        case _ => throw DeserializationException("VerboseBest expected")
      }
  }

}