package kaimere.real.optimization.general

import kaimere.real.objects
import kaimere.real.objects.{Function, RealVector}
import kaimere.real.optimization._
import kaimere.real.optimization.general.MetaOptimizationAlgorithm.MOA_State
import kaimere.real.optimization.general.OptimizationAlgorithm.Area
import kaimere.real.optimization.general.instructions.GeneralInstruction
import kaimere.tools.random.GoRN
import spray.json._

case class MetaOptimizationAlgorithm(algorithms: Seq[OptimizationAlgorithm],
                                     targetVars: Seq[Option[Set[String]]],
                                     instructions: Seq[GeneralInstruction]) extends OptimizationAlgorithm {

  protected var algorithmArea: Seq[OptimizationAlgorithm.Area] = Seq.empty

  override def initializeRandomState(): State = {
    val v = GoRN.getContinuousUniform(area)
    MOA_State(v)
  }

  override def initializeFromGivenState(state: Vector[Map[String, Double]]): State = {
    val realVectors = Helper.prepareInitialState(state)
    val bestVector = Helper.chooseOneBest(realVectors, f)
    MOA_State(bestVector)
  }

  override def iterate(): Unit = ???

  override def initialize(f: objects.Function, area: Area, state: Option[Vector[Map[String, Double]]]): Unit = {
    super.initialize(f, area, state)
    algorithmArea = targetVars.map {
      case Some(vars) => vars.map(key => (key, area(key))).toMap[String, (Double, Double)]
      case None => area
    }

  }

  override def work(instruction: GeneralInstruction): RealVector = {
    val MOA_State(initialSeed) = currentState
    algorithms.indices.foldLeft(initialSeed) { case (seed, id) =>
      println(s"Processing ${id + 1}/${algorithms.size}")
        val tempArea = seed.vals.map { case (key, v) => (key, (v, v)) } ++ algorithmArea(id)
        algorithms(id).initialize(f, tempArea, state = Some(Vector(seed.vals)))
        val tempResult = algorithms(id).work(instructions(id))
        currentState = MOA_State(tempResult)
        tempResult
    }
  }

}

object MetaOptimizationAlgorithm {

  case class MOA_State(v: RealVector) extends State {

    override def toVectors(): Vector[RealVector] = Vector(v)

    override def getBestBy(f: Function): (RealVector, Double) = (v, f(v))

  }

  implicit object MetaOptimizationAlgorithmJsonFormat extends RootJsonFormat[MetaOptimizationAlgorithm] {
    def write(moa: MetaOptimizationAlgorithm) =
      JsObject(
        "name" -> JsString("MetaOptimizationAlgorithm"),
        "algorithms" -> JsArray(moa.algorithms.map(OptimizationAlgorithm.toJson).toVector),
        "targetVars" -> JsArray(moa.targetVars.map {
          case None => JsString("all")
          case Some(vars) => JsString(vars.mkString(","))
        }.toVector),
        "instructions" -> JsArray(moa.instructions.map(GeneralInstruction.toJson).toVector))

    def read(json: JsValue): MetaOptimizationAlgorithm =
      json.asJsObject.getFields("name", "algorithms", "targetVars", "instructions") match {
        case Seq(JsString(name), JsArray(algorithms), JsArray(targetVars), JsArray(instructions)) =>
          if (name != "MetaOptimizationAlgorithm") throw DeserializationException("MetaOptimizationAlgorithm expected")
          else MetaOptimizationAlgorithm(
            algorithms = algorithms.map(OptimizationAlgorithm.fromJson),
            targetVars = targetVars.map {
              case JsString("all") => Option.empty[Set[String]]
              case JsString(vars) => Some(vars.split(",").toSet)
            },
            instructions = instructions.map(GeneralInstruction.fromJson))
        case _ => throw DeserializationException("MetaOptimizationAlgorithm expected")
      }
  }

}