package kaimere.real.optimization.metaheuristic

import kaimere.real.optimization.general._
import kaimere.real.objects.{Function, RealVector}
import kaimere.real.objects.RealVector._
import kaimere.real.optimization.metaheuristic.CatSwarmOptimization.{Cat, CSO_State}
import kaimere.tools.random.GoRN
import kaimere.tools.etc._
import spray.json._

case class CatSwarmOptimization
(numberOfCats: Int, MR: Double,
 SMP: Int, SRD: Double, CDC: Int, SPC: Boolean,
 velocityConstant: Double, velocityRatio: Double) extends OptimizationAlgorithm {

  private var maxVelocity: Map[String, (Double, Double)] = Map.empty

  override def initializeRandomState(): State = {
    (1 to numberOfCats).map { _ =>
      val location = GoRN.getContinuousUniform(area)
      val velocity = GoRN.getContinuousUniform(maxVelocity)
      Cat(location, velocity, f(location))
    } |> CSO_State
  }

  override def initializeFromGivenState(state: Vector[Map[String, Double]]): State = {
    val idsChosen = GoRN.getFromSeries(state.indices, numberOfCats, withReturn = true)
    idsChosen.map(id => Cat.createRandomCat(state(id), f, area, maxVelocity)) |> CSO_State
  }

  override def initialize(f: Function, area: OptimizationAlgorithm.Area,
                          state: Option[Vector[Map[String, Double]]]): Unit = {
    maxVelocity = area.map{ case (key, (min, max)) => (key, (-velocityRatio * (max - min), velocityRatio * (max - min))) }
    super.initialize(f, area, state)
  }

  override def iterate(): Unit = {
    val CSO_State(catPack) = currentState
    val bestCat = catPack.minBy(_.fitness)
    currentState =
      catPack.indices.map { id =>
        catPack(id).move(
          if (GoRN.getContinuousUniform(0.0, 1.0) <= MR) 0 else 1,
          f, area, bestCat,
          SPC, SMP, CDC, SRD,
          velocityConstant, maxVelocity)
      } |> CSO_State.apply
  }

}

object CatSwarmOptimization {

  protected case class Cat(location: RealVector, velocity: RealVector, fitness: Double) {

    def seek(f: Function, area: OptimizationAlgorithm.Area, SPC: Boolean, SMP: Int, CDC: Int, SRD: Double): Cat = {

      val newLocations = (if (SPC) Seq(location) else Seq()) ++
        Seq.fill(SMP - (if (SPC) 1 else 0))(location)
          .map { loc =>
            val ratio =GoRN.getFromSeries(area.keys.toSeq, CDC, false)
              .map { key => (key, GoRN.getContinuousUniform(1.0 - SRD, 1.0 + SRD)) }.toMap
            (loc ~* ratio).constrain(area)
          }

      val fitnessValues = newLocations.map(f(_))
      val newLocation =
        if (fitnessValues.tail.forall(_ == fitnessValues.head)) newLocations(GoRN.getDiscreteUniform(0, SMP - 1))
        else {
          val maxFitness = fitnessValues.max
          val minFitness = fitnessValues.min
          val probabilities = fitnessValues.map(v => (maxFitness - v) / (maxFitness - minFitness))
          val roulette =
            0.0 +: probabilities.tail
              .foldLeft(Seq(probabilities.head)) { case (prob, curr) => (curr + prob.head) +: prob }
              .reverse
          val chosen = GoRN.getContinuousUniform(0.0, roulette.last)
          val idChosen = roulette.sliding(2).indexWhere{ case Seq(a, b) => a <= chosen && chosen <= b}
          newLocations(idChosen)
        }
      new Cat(newLocation, newLocation - this.location, f(newLocation))
    }

    def updateVelocity(bestCat: Cat, velocityConstant: Double, maxVelocity: Map[String, (Double, Double)]): RealVector = {
      val newVelocity = this.velocity + (bestCat.location - this.location) * velocityConstant * GoRN.getContinuousUniform(0.0, 1.0)
      newVelocity.constrain(maxVelocity)
    }

    def trace(f: Function, area: OptimizationAlgorithm.Area, bestCat: Cat, velocityConstant: Double, maxVelocity: Map[String, (Double, Double)]): Cat = {
      val newVelocity = this.updateVelocity(bestCat, velocityConstant, maxVelocity)
      val newLocation = (location + newVelocity).constrain(area)
      new Cat(newLocation, newVelocity, f(newLocation))
    }

    def move(mode: Int, f: Function, area: OptimizationAlgorithm.Area, bestCat: Cat,
             SPC: Boolean, SMP: Int, CDC: Int, SRD: Double,
             velocityConstant: Double, maxVelocity: Map[String, (Double, Double)]): Cat = mode match {
      case 0 => seek(f, area, SPC, SMP, CDC, SRD)
      case 1 => trace(f, area, bestCat, velocityConstant, maxVelocity)
    }
  }

  protected object Cat {

    def createRandomCat(location: RealVector,f: Function, area: OptimizationAlgorithm.Area, maxVelocity: Map[String, (Double, Double)]): Cat = {
      new Cat(location, RealVector(GoRN.getContinuousUniform(maxVelocity)), f(location))
    }
  }

  protected case class CSO_State(cats: Seq[Cat]) extends State  {

    override def toVectors(): Vector[RealVector] = cats.map(_.location).toVector

    def getBestBy(f: Function): RealVector = cats.minBy(_.fitness).location

    def apply(id: Int): Cat = cats(id)

  }

  implicit object CatSwarmOptimizationJsonFormat extends RootJsonFormat[CatSwarmOptimization] {
    def write(cso: CatSwarmOptimization) =
      JsObject(
        "name" -> JsString("CatSwarmOptimization"),
        "numberOfCats" -> JsNumber(cso.numberOfCats),
        "MR" -> JsNumber(cso.MR),
        "SMP" -> JsNumber(cso.SMP),
        "SRD" -> JsNumber(cso.SRD),
        "CDC" -> JsNumber(cso.CDC),
        "SPC" -> JsBoolean(cso.SPC),
        "velocityConstant" -> JsNumber(cso.velocityConstant),
        "velocityRatio" -> JsNumber(cso.velocityRatio))

    def read(json: JsValue): CatSwarmOptimization =
      json.asJsObject.getFields("name", "numberOfCats", "MR", "SMP", "SRD", "CDC", "SPC", "velocityConstant", "velocityRatio") match {
        case Seq(JsString(name), JsNumber(numberOfCats), JsNumber(mr), JsNumber(smp), JsNumber(srd), JsNumber(cdc), JsBoolean(spc), JsNumber(velocityConstant), JsNumber(velocityRatio)) =>
          if (name != "CatSwarmOptimization") throw DeserializationException("CatSwarmOptimization expected")
          else CatSwarmOptimization(numberOfCats.toInt, mr.toDouble, smp.toInt, srd.toDouble, cdc.toInt, spc, velocityConstant.toDouble, velocityRatio.toDouble)
        case _ => throw DeserializationException("CatSwarmOptimization expected")
      }
  }

}
