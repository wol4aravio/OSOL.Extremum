package OSOL.Extremum.Cores.JVM.Optimization

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.Optimization.Exceptions.ParameterAlreadyExistsException
import OSOL.Extremum.Cores.JVM.Optimization.Nodes.{GeneralNode, SetParametersNode, TerminationViaMaxIterations, TerminationViaMaxTime}
import OSOL.Extremum.Cores.JVM.Optimization.Testing.{IntervalTester, RealTester}
import OSOL.Extremum.Cores.JVM.Random.GoRN
import OSOL.Extremum.Cores.JVM.Vectors.{IntervalVector, RealVector}
import org.scalatest.FunSuite

class GeneralOptimizationSuite extends FunSuite {

  val fReal: Map[String, Double] => Double = (v: Map[String, Double]) => math.abs(v("x"))
  val fInterval: Map[String, Interval] => Interval = (v: Map[String, Interval]) => v("x").abs()
  val area: Area = Map("x" -> (-10.0, 10.0))

  test("TerminationViaMaxIterations") {
    val node = new TerminationViaMaxIterations[RealVector, Double, RealVector](nodeId = 1, maxIteration = 250)
    val state: State[RealVector, Double, RealVector] = new State[RealVector, Double, RealVector]()

    node.initialize(fReal, area, state)
    intercept[ParameterAlreadyExistsException] { node.initialize(fReal, area, state) }
  }
  test("TerminationViaMaxTime") {
    val node = new TerminationViaMaxTime[IntervalVector, Interval, IntervalVector](nodeId = 1, maxTime = 1.0)
    val state: State[IntervalVector, Interval, IntervalVector] = new State[IntervalVector, Interval, IntervalVector]()

    node.initialize(fInterval, area, state)
    intercept[ParameterAlreadyExistsException] { node.initialize(fInterval, area, state) }
  }

}
