package kaimere.real.optimization.general.instructions

import kaimere.real.optimization.general.OptimizationAlgorithm
import spray.json._

trait GeneralInstruction {

  def continue(algorithm: OptimizationAlgorithm): Boolean
  def reset(): Unit

}

object GeneralInstruction {

  def toJson(instruction: GeneralInstruction): JsValue = {
    instruction match {
      case mi: MaxIterations => mi.toJson
      case mt: MaxTime => mt.toJson
      case tv: TargetValue => tv.toJson
      case vb: VerboseBest => vb.toJson
      case _ => throw new Exception("Unsupported Instruction")
    }
  }

  def fromJson(json: JsValue): GeneralInstruction = {
    json.asJsObject.getFields("name") match {
      case Seq(JsString(name)) =>
        name match {
          case "MaxIterations" => json.convertTo[MaxIterations]
          case "MaxTime" => json.convertTo[MaxTime]
          case "TargetValue" => json.convertTo[TargetValue]
          case "VerboseBest" => json.convertTo[VerboseBest]
          case _ => throw DeserializationException("Unsupported Instruction")
        }
      case _ => throw DeserializationException("Instruction expected")
    }
  }

}