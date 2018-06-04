package OSOL.Extremum.Cores.JVM.Optimization.Testing

import java.io.File

import OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions.RemoteFunction
import OSOL.Extremum.Cores.JVM.Optimization.{Algorithm, Area, Optimizable}
import OSOL.Extremum.Cores.JVM.Vectors.{RealVector, VectorObject}
import OSOL.Extremum.Cores.JVM.Optimization.{Algorithm, Optimizable}
import OSOL.Extremum.Cores.JVM.Vectors.VectorObject

abstract class Tester[Base, FuncType, V <: Optimizable[Base, FuncType]](testFunctions: Seq[RemoteFunction[FuncType]],
                                                                        areas: Seq[Area],
                                                                        solutions: Seq[Map[String, java.lang.Double]],
                                                                        tolerance: java.lang.Double,
                                                                        attempts: java.lang.Integer) {

  def Lp_norm(v1: VectorObject[java.lang.Double], v2: VectorObject[java.lang.Double], p: java.lang.Integer = 2): java.lang.Double = {
    val keys = v1.keys ++ v2.keys
    keys.map(k => math.pow(math.abs(v1(k) - v2(k)), p.doubleValue())).sum
  }

  def apply(algorithms: Algorithm[Base, FuncType, V]*): java.lang.Boolean = {
    val resultsPerFunction = testFunctions.zip(areas).zip(solutions)
      .map { case ((f, area), sol) => {
        var success = false
        val resultsPerAlgorithm = algorithms.takeWhile { a => {
          val resultsPerAttempt = (1 to attempts).takeWhile { _ =>
            a.reset()
            f.initialize()
            val r = a.work(f.apply, area, logStates = Some("temp")).toBasicForm()
            f.terminate()

            val tempFolder = new File("temp")
            if (!(tempFolder.exists && tempFolder.isDirectory)) throw new Exception("Logging failed")
            tempFolder.listFiles().foreach(_.delete())
            tempFolder.delete()

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
