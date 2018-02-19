package kaimere.real.optimization.general.instructions

import MaxTime._
import MaxIterations._
import TargetValue._
import AllInstruction._
import AnyInstruction._
import StateLogger._
import VerboseBest._

import org.scalatest.FunSuite
import spray.json._

class InstructionSerializationSuite extends FunSuite {

  private val maxTime = "MaxTime,10.0,true"
  private val maxIterations = "MaxIterations,1000,true"
  private val targetValue = "TargetValue,0.0,0.01,true"
  private val allInstruction = "AllInstruction,MaxTime,10.0,true&MaxIterations,1000,true"
  private val anyInstruction = "AnyInstruction,MaxTime,10.0,true|MaxIterations,1000,true"
  private val stateLogger = "StateLogger,temp,true,MaxTime,10.0,true"
  private val verboseBest = "VerboseBest,MaxTime,10.0,true"

  def testInstructionSerialization[T <: Instruction](csv: String): Boolean = {

    val instruction: T = Instruction.fromCsv(csv).asInstanceOf[T]
    val json = Instruction.toJson(instruction)
    val fromJson: T = Instruction.fromJson(json).asInstanceOf[T]

    instruction == fromJson

  }

  test("MaxTime Serialization") {
    assert(testInstructionSerialization[MaxTime](maxTime))
  }

  test("MaxIterations Serialization") {
    assert(testInstructionSerialization[MaxIterations](maxIterations))
  }

  test("TargetValue Serialization") {
    assert(testInstructionSerialization[TargetValue](targetValue))
  }

  test("AllInstruction Serialization") {
    assert(testInstructionSerialization[AllInstruction](allInstruction))
  }

  test("AnyInstruction Serialization") {
    assert(testInstructionSerialization[AnyInstruction](anyInstruction))
  }

  test("StateLogger Serialization") {
    assert(testInstructionSerialization[StateLogger](stateLogger))
  }

  test("VerboseBest Serialization") {
    assert(testInstructionSerialization[VerboseBest](verboseBest))
  }

  test("MaxTime Bad Serialization (csv)") {
    assert(
      try { val instruction: MaxTime = MaxTime(maxIterations); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("MaxIterations Bad Serialization (csv)") {
    assert(
      try { val instruction: MaxIterations = MaxIterations(targetValue); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("TargetValue Bad Serialization (csv)") {
    assert(
      try { val instruction: TargetValue = TargetValue(allInstruction); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("AllInstruction Bad Serialization (csv)") {
    assert(
      try { val instruction: AllInstruction = AllInstruction(anyInstruction); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("AnyInstruction Bad Serialization (csv)") {
    assert(
      try { val instruction: AnyInstruction = AnyInstruction(stateLogger); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("StateLogger Bad Serialization (csv)") {
    assert(
      try { val instruction: StateLogger = StateLogger(verboseBest); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("VerboseBest Bad Serialization (csv)") {
    assert(
      try { val instruction: VerboseBest = VerboseBest(maxTime); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("MaxTime Bad Serialization (json)") {
    assert(
      try { val instruction: MaxTime = MaxIterations(maxIterations).toJson.convertTo[MaxTime]; false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("MaxIterations Bad Serialization (json)") {
    assert(
      try { val instruction: MaxIterations = TargetValue(targetValue).toJson.convertTo[MaxIterations]; false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("TargetValue Bad Serialization (json)") {
    assert(
      try { val instruction: TargetValue = AllInstruction(allInstruction).toJson.convertTo[TargetValue]; false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("AllInstruction Bad Serialization (json)") {
    assert(
      try { val instruction: AllInstruction = AnyInstruction(anyInstruction).toJson.convertTo[AllInstruction]; false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("AnyInstruction Bad Serialization (json)") {
    assert(
      try { val instruction: AnyInstruction = StateLogger(stateLogger).toJson.convertTo[AnyInstruction]; false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("StateLogger Bad Serialization (json)") {
    assert(
      try { val instruction: StateLogger = VerboseBest(verboseBest).toJson.convertTo[StateLogger]; false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("VerboseBest Bad Serialization (json)") {
    assert(
      try { val instruction: VerboseBest = MaxTime(maxTime).toJson.convertTo[VerboseBest]; false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

}
