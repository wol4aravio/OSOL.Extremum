package OSOL.Extremum.Cores.JVM.Optimization.Testing

import OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions.RemoteFunction
import OSOL.Extremum.Cores.JVM.Optimization.{Algorithm, Area, Optimizable}
import OSOL.Extremum.Cores.JVM.Vectors.{RealVector, VectorObject}
import OSOL.Extremum.Cores.JVM.Optimization.{Algorithm, Optimizable}
import OSOL.Extremum.Cores.JVM.Vectors.VectorObject

abstract class Tester[Base, FuncType, V <: Optimizable[Base, FuncType]](testFunctions: Seq[RemoteFunction[FuncType]],
                                                                        areas: Seq[Area],
                                                                        solutions: Seq[Map[String, Double]],
                                                                        tolerance: Double,
                                                                        attempts: Int) {

  def Lp_norm(v1: VectorObject[Double], v2: VectorObject[Double], p: Int = 2): Double = {
    val keys = v1.keys ++ v2.keys
    keys.map(k => math.pow(math.abs(v1(k) - v2(k)), p)).sum
  }

  def apply(algorithms: Algorithm[Base, FuncType, V]*): Boolean = {
    val resultsPerFunction = testFunctions.zip(areas).zip(solutions)
      .map { case ((f, area), sol) => {
        var success = false
        val resultsPerAlgorithm = algorithms.takeWhile { a => {
          val resultsPerAttempt = (1 to attempts).takeWhile { _ =>
            a.reset()
            f.initialize()
            val r = a.work(f.apply, area).toBasicForm()
            f.terminate()
            success = Lp_norm(r, RealVector(sol)) < tolerance
            !success
          }
          !success
        }
        }
        success
      }
      }
    resultsPerFunction.forall(r => r)
  }

}
