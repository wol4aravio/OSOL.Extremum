package OSOL.Extremum.Cores.JVM.Cybernatics

import OSOL.Extremum.Cores.JVM.Vectors.VectorObject

abstract class DynamicSystem[Base](f: VectorObject[Base] => VectorObject[Base], u: VectorObject[Base] => VectorObject[Base], butcherTableau: ButcherTableau) {

  implicit def doubleToBase(d: Double): Base
  implicit def baseToDouble(b: Base): Double

  final def prolong(currentTime: Double, currentState: VectorObject[Base], controls: VectorObject[Base], eps: Double): VectorObject[Base] = {
    val kElements = (2 to butcherTableau.numberOfParts)
      .foldLeft(Map(1 -> f(currentState.union((controls.elements + ("t" -> doubleToBase(currentTime))).toSeq:_*)))) {
      case (previous, i) =>
        val newTime: Base = currentTime + eps * butcherTableau.getC(i)
        val newState = currentState + (1 to (i - 1)).map { j => previous(j) * butcherTableau.getA(i, j) }.reduce(_ + _) * eps
        val newK = f(newState.union((controls.elements + ("t" -> newTime)).toSeq:_*))
        previous + (i -> newK)
    }
    currentState + kElements.map { case (i, k) => k * butcherTableau.getB(i) }.reduce(_ + _) * eps
  }

  final def simulate(initialCondition: VectorObject[Base], eps: Double, terminationConditions: Map[String, (Double, Double)], maxSteps: Int, maxOverallError: Double): (Seq[Double], Seq[VectorObject[Base]], Seq[VectorObject[Base]]) = {
    var stop = false
    val (times, states, controls) = (1 to maxSteps).foldLeft((Seq(0.0), Seq(initialCondition), Seq.empty[VectorObject[Base]])) {
      case ((_times, _states, _controls), stepId) =>
        if (!stop) {
          val currentTime = _times.head
          val currentState = _states.head
          val control = u(currentState.union("t" -> doubleToBase(currentTime)))
          val newState = prolong(currentTime, currentState, control, eps)
          val newTime: Base = eps * stepId
          val terminalConditionError = newState.union((control.elements + ("t" -> newTime)).toSeq:_*).distanceFromArea(terminationConditions)
          stop = terminalConditionError.values.sum <= maxOverallError
          (baseToDouble(newTime) +: _times, newState +: _states, control +: _controls)
        }
        else (_times.reverse, _states.reverse, _controls.reverse)
    }
    (times.reverse, states.reverse, controls.reverse)
  }

}
