package OSOL.Extremum.Cores.JVM.Cybernatics

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.Vectors.VectorObject

class IntervalValuedDynamicSystem(f: VectorObject[Interval] => VectorObject[Interval], u: VectorObject[Interval] => VectorObject[Interval], butcherTableau: ButcherTableau)
  extends DynamicSystem[Interval](f, u, butcherTableau) {

  final override implicit def doubleToBase(d: Double): Interval = Interval(d)

  final override implicit def baseToDouble(b: Interval): Double = b.middlePoint

}
