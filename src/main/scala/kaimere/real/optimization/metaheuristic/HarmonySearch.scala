package kaimere.real.optimization.metaheuristic

import kaimere.real.objects.{Function, RealVector}
import kaimere.real.optimization.Helper
import kaimere.real.optimization.general.initializers.Initializer
import kaimere.real.optimization.general.{OptimizationAlgorithm, State}
import kaimere.real.optimization.metaheuristic.HarmonySearch._
import kaimere.tools.random.GoRN
import kaimere.tools.etc._
import spray.json._

case class HarmonySearch(numberOfHarmonics: Int, memoryAcceptRate: Double, pitchAdjustingRate: Double, bandwidthRatio: Double) extends OptimizationAlgorithm {

  private var possibleDelta: Map[String, (Double, Double)] = Map.empty

  override def initializeFromGivenState(state: State): State = {
    val realVectors = Helper.prepareInitialState(state)
    val bestVectors = Helper.chooseSeveralBest(realVectors, f, numberOfHarmonics)
    bestVectors.map(v => Harmonic(v, f(v))).toVector |> HS_State.apply
  }

  override def initialize(f: Function, area: OptimizationAlgorithm.Area,
                          state: Option[State], initializer: Initializer): Unit = {
    possibleDelta = area.map { case (key, value) =>
      val width: Double = value._2 - value._1
      (key, (-bandwidthRatio * width, bandwidthRatio * width))
    }
    super.initialize(f, area, state, initializer)
  }

  override def iterate(): Unit = {
    val HS_State(harmonics) = currentState

    val idChosen = GoRN.getFromSeries(Range(0, numberOfHarmonics), 1, withReturn = false).head
    val newHarmonicLocation = harmonics(idChosen).location.vals.map {
      case (key, value) =>
        val newValue =
          if (GoRN.getContinuousUniform(0.0, 1.0) < memoryAcceptRate) {
            if (GoRN.getContinuousUniform(0.0, 1.0) < pitchAdjustingRate)
              value + (possibleDelta(key) |> Function.tupled(GoRN.getContinuousUniform))
            else value
          }
          else this.area(key) |> Function.tupled(GoRN.getContinuousUniform)
        (key, newValue)
    }
    val newHarmonicFitness = this.f(newHarmonicLocation)
    val worstFitness = harmonics.map(_.fitness).max
    val idWorst = harmonics.indexWhere(_.fitness == worstFitness)
    currentState = (harmonics.zipWithIndex.filter { case (_, id) => id != idWorst }.map(_._1) :+ Harmonic(newHarmonicLocation, newHarmonicFitness)) |> HS_State
  }

}

object HarmonySearch {

  def apply(csv: String): HarmonySearch = {
    val Array(name, numberOfHarmonics, memoryAcceptRate, pitchAdjustingRate, bandwidthRatio) = csv.split(",")
    name match {
      case "HS" | "hs" | "HarmonySearch" => HarmonySearch(numberOfHarmonics.toInt, memoryAcceptRate.toDouble, pitchAdjustingRate.toDouble, bandwidthRatio.toDouble)
      case _ => throw DeserializationException("HarmonySearch expected")
    }
  }

  case class Harmonic(location: RealVector, fitness: Double)

  case class HS_State(harmonics: Vector[Harmonic]) extends State(vectors = harmonics.map(_.location))

  implicit object HarmonySearchJsonFormat extends RootJsonFormat[HarmonySearch] {
    def write(hs: HarmonySearch) =
      JsObject(
        "name" -> JsString("HarmonySearch"),
        "numberOfHarmonics" -> JsNumber(hs.numberOfHarmonics),
        "memoryAcceptRate" -> JsNumber(hs.memoryAcceptRate),
        "pitchAdjustingRate" -> JsNumber(hs.pitchAdjustingRate),
        "bandwidthRatio" -> JsNumber(hs.bandwidthRatio))

    def read(json: JsValue): HarmonySearch =
      json.asJsObject.getFields("name", "numberOfHarmonics", "memoryAcceptRate", "pitchAdjustingRate", "bandwidthRatio") match {
        case Seq(JsString(name), JsNumber(numberOfHarmonics), JsNumber(memoryAcceptRate), JsNumber(pitchAdjustingRate), JsNumber(bandwidthRatio)) =>
          if (name != "HarmonySearch") throw DeserializationException("HarmonySearch expected")
          else HarmonySearch(Seq(name, numberOfHarmonics.toInt, memoryAcceptRate, pitchAdjustingRate, bandwidthRatio).mkString(","))
        case _ => throw DeserializationException("HarmonySearch expected")
      }
  }

}