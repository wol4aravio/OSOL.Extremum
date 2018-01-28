package kaimere.real

import kaimere.real.optimization.general._
import kaimere.real.objects.{RealVector, Function}

package object optimization {

  object Tester {

    def normVector(vector: RealVector): Double =
      math.sqrt(vector.vals.foldLeft(0.0) { case (sum, (_, value)) => sum + value * value })

    @scala.annotation.tailrec
    def apply(tool: OptimizationAlgorithm,
              f: Function, area: OptimizationAlgorithm.Area,
              state: Option[Vector[Map[String, Double]]],
              instruction: Instruction, epsNorm: Double, maxTries: Int): Boolean = {
      tool.initialize(f, area, state)
      val result = tool.work(instruction)
      if (normVector(result) < epsNorm)
        true
      else {
        if (maxTries == 0)
          false
        else
          Tester(tool, f, area, state, instruction, epsNorm, maxTries - 1)
      }
    }

  }

  object DummyFunctions {

    class DummyFunction(f: Map[String, Double] => Double) extends Function {
      override def apply(vector: RealVector): Double = f(vector.vals)
    }

    val area_1: OptimizationAlgorithm.Area = Map("x" -> (-10.0, 10.0))
    val func_1 = new DummyFunction((v: Map[String, Double]) => v("x") * v("x"))

    val area_2: OptimizationAlgorithm.Area = Map("x" -> (-10.0, 10.0), "y" -> (-10.0, 10.0))
    val func_2 = new DummyFunction((v: Map[String, Double]) => v("x") * v("x") + v("y") * v("y"))

    val area_3: OptimizationAlgorithm.Area = Map("x" -> (-10.0, 10.0), "y" -> (-10.0, 10.0), "z" -> (-10.0, 10.0))
    val func_3 = new DummyFunction((v: Map[String, Double]) => v("x") * v("x") + v("y") * v("y") + v("z") * v("z"))

  }

}
