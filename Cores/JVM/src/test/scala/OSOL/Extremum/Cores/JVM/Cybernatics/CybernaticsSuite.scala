package OSOL.Extremum.Cores.JVM.Cybernatics

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.Arithmetics.Interval.Converters._
import OSOL.Extremum.Cores.JVM.Vectors.{RealVector, VectorObject}
import OSOL.Extremum.Cores.JVM.Vectors.IntervalVector.Converters._
import OSOL.Extremum.Cores.JVM.Vectors.RealVector.Converters._
import org.scalatest.FunSuite

class CybernaticsSuite extends FunSuite {

  val historyGenerator: VectorObject[Double] => VectorObject[Double] = v => Map("x1" -> (1.0 - math.cos(v("t"))), "x2" -> math.sin(v("t")), "x3" -> (1.0 + v("t") - math.sin(v("t")) - math.cos(v("t"))))

  val fRealPure: VectorObject[Double] => VectorObject[Double] = v => Map("x1" -> math.sin(v("t")), "x2" -> math.cos(v("t")), "x3" -> (v("x1") + v("x2")))
  val uRealPure: VectorObject[Double] => VectorObject[Double] = v => Map.empty

  val fIntervalPure: VectorObject[Interval] => VectorObject[Interval] = v => Map("x1" -> v("t").sin(), "x2" -> v("t").cos(), "x3" -> (v("x1") + v("x2")))
  val uIntervalPure: VectorObject[Interval] => VectorObject[Interval] = v => Map.empty

  val fRealViaControl: VectorObject[Double] => VectorObject[Double] = v => Map("x1" -> math.sin(v("u1")), "x2" -> math.cos(v("u2")), "x3" -> (v("x1") + v("x2")))
  val uRealViaControl: VectorObject[Double] => VectorObject[Double] = v => Map("u1" -> v("t"), "u2" -> v("t"))

  val fIntervalViaControl: VectorObject[Interval] => VectorObject[Interval] = v => Map("x1" -> v("u1").sin(), "x2" -> v("u2").cos(), "x3" -> (v("x1") + v("x2")))
  val uIntervalViaControl: VectorObject[Interval] => VectorObject[Interval] = v => Map("u1" -> v("t"), "u2" -> v("t"))

  val maxSteps = 1000
  val eps = 1e-2
  val area = Map("t" -> (1.0 - 1e-5, 1.0 + 1e-5))
  val tol = 1e-7



  test("Test: Real")
  {
    val initialState = Map("x1" -> 0.0, "x2" -> 0.0, "x3" -> 0.0)
    val idealStates = Range(0, (1.0 / eps).toInt + 1).map(t => historyGenerator(Map("t" -> t * eps)))

    val dsRealEuler = new RealValuedDynamicSystem(fRealPure, uRealPure, ButcherTableau.getEuler)
    val (_, generatedStatesEuler, _) = dsRealEuler.simulate(initialState, eps, area, maxSteps, maxOverallError = 1e-7)
    val averageErrorEuler = generatedStatesEuler.zip(idealStates)
      .map { case (v1, v2) => (v1.toBasicForm() - v2.elements).elements.values.map(math.abs)}
      .map(e => e.sum / e.size)
      .sum / generatedStatesEuler.size

    val dsRealRK4_Pure = new RealValuedDynamicSystem(fRealPure, uRealPure, ButcherTableau.getRK4)
    val (_, generatedStatesRK4_Pure, _) = dsRealRK4_Pure.simulate(initialState, eps, area, maxSteps, maxOverallError = 1e-7)
    val averageErrorRK4_Pure = generatedStatesRK4_Pure.zip(idealStates)
      .map { case (v1, v2) => (v1.toBasicForm() - v2.elements).elements.values.map(math.abs)}
      .map(e => e.sum / e.size)
      .sum / generatedStatesRK4_Pure.size

    val dsRealRK4_ViaControl = new RealValuedDynamicSystem(fRealViaControl, uRealViaControl, ButcherTableau.getRK4)
    val (_, generatedStatesRK4_ViaControl, _) = dsRealRK4_ViaControl.simulate(initialState, eps, area, maxSteps, maxOverallError = 1e-7)
    val averageErrorRK4_ViaControl = generatedStatesRK4_ViaControl.zip(idealStates)
      .map { case (v1, v2) => (v1.toBasicForm() - v2.elements).elements.values.map(math.abs)}
      .map(e => e.sum / e.size)
      .sum / generatedStatesRK4_ViaControl.size

    assert(averageErrorEuler > averageErrorRK4_Pure)
    assert(averageErrorRK4_ViaControl > averageErrorRK4_Pure)
    assert(averageErrorRK4_Pure < tol)
  }

  test("Test: Interval")
  {
    val initialState = Map("x1" -> Interval(0.0), "x2" -> Interval(0.0), "x3" -> Interval(0.0))
    val idealStates = Range(0, (1.0 / eps).toInt + 1).map(t => historyGenerator(Map("t" -> t * eps)))

    val dsIntervalEuler = new IntervalValuedDynamicSystem(fIntervalPure, uIntervalPure, ButcherTableau.getEuler)
    val (_, generatedStatesEuler, _) = dsIntervalEuler.simulate(initialState, eps, area, maxSteps, maxOverallError = 1e-7)
    val averageErrorEuler = generatedStatesEuler.zip(idealStates)
      .map { case (v1, v2) => (v1.toBasicForm() - v2.elements).elements.values.map(math.abs)}
      .map(e => e.sum / e.size)
      .sum / generatedStatesEuler.size

    val dsIntervalRK4_Pure = new IntervalValuedDynamicSystem(fIntervalPure, uIntervalPure, ButcherTableau.getRK4)
    val (_, generatedStatesRK4_Pure, _) = dsIntervalRK4_Pure.simulate(initialState, eps, area, maxSteps, maxOverallError = 1e-7)
    val averageErrorRK4_Pure = generatedStatesRK4_Pure.zip(idealStates)
      .map { case (v1, v2) => (v1.toBasicForm() - v2.elements).elements.values.map(math.abs)}
      .map(e => e.sum / e.size)
      .sum / generatedStatesRK4_Pure.size

    val dsIntervalRK4_ViaControl = new IntervalValuedDynamicSystem(fIntervalViaControl, uIntervalViaControl, ButcherTableau.getRK4)
    val (_, generatedStatesRK4_ViaControl, _) = dsIntervalRK4_ViaControl.simulate(initialState, eps, area, maxSteps, maxOverallError = 1e-7)
    val averageErrorRK4_ViaControl = generatedStatesRK4_ViaControl.zip(idealStates)
      .map { case (v1, v2) => (v1.toBasicForm() - v2.elements).elements.values.map(math.abs)}
      .map(e => e.sum / e.size)
      .sum / generatedStatesRK4_ViaControl.size

    assert(averageErrorEuler > averageErrorRK4_Pure)
    assert(averageErrorRK4_ViaControl > averageErrorRK4_Pure)
    assert(averageErrorRK4_Pure < tol)
  }

}
