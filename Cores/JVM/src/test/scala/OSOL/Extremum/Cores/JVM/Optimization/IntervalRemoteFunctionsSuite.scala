package OSOL.Extremum.Cores.JVM.Optimization

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions._
import org.scalatest.FunSuite

class IntervalRemoteFunctionsSuite extends FunSuite {

  test("Dummy Interval f") {

    val f = new IntervalRemoteFunction(json = s"${sys.env("OSOL_EXTREMUM_TASKS_LOC")}/Dummy/Dummy_3.json", port = 5000, field = "f")
    f.initialize()
    val result = f(Map("x" -> Interval(1.0, 2.0), "y" -> Interval(2.0, 3.0), "z" -> Interval(3.0, 4.0)))
    f.terminate()

    assert(result equalsTo Interval(36.0, 70.0))
    Thread.sleep(5000)

  }

}
