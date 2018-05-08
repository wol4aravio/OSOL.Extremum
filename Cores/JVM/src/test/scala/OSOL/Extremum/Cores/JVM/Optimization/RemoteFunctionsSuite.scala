package OSOL.Extremum.Cores.JVM.Optimization

import org.scalatest.FunSuite

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions._

class RemoteFunctionsSuite extends FunSuite {

  test("Dummy Real f") {

    val f = new RealRemoteFunction(json = s"${sys.env("TASKS_LOC")}/Dummy/Dummy_3.json", port = 5000, field = "f")
    f.initialize()
    val result = f(Map("x" -> 1.0, "y" -> 2.0, "z" -> 3.0))
    f.terminate()

    assert(result == 36.0)

  }

  test("Dummy Interval f") {

    val f = new IntervalRemoteFunction(json = s"${sys.env("TASKS_LOC")}/Dummy/Dummy_3.json", port = 5000, field = "f")
    f.initialize()
    val result = f(Map("x" -> Interval(1.0, 2.0), "y" -> Interval(2.0, 3.0), "z" -> Interval(3.0, 4.0)))
    f.terminate()

    assert(result equalsTo Interval(36.0, 70.0))

  }

}
