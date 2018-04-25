package OSOL.Extremum.Cores.JVM.Cybernatics

import OSOL.Extremum.Cores.JVM.Vectors.VectorObject

class RealValuedDynamicSystem(f: VectorObject[Double] => VectorObject[Double], u: VectorObject[Double] => VectorObject[Double], butcherTableau: ButcherTableau)
  extends DynamicSystem[Double](f, u, butcherTableau) {

  final override implicit def doubleToBase(d: Double): Double = d

  final override implicit def baseToDouble(b: Double): Double = b

}
