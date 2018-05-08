package OSOL.Extremum.Cores.JVM.Optimization

import org.scalatest.FunSuite

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions._

class RealRemoteFunctionsSuite extends FunSuite {

  test("Dummy Real f") {

    val f = new RealRemoteFunction(json = s"${sys.env("OSOL_EXTREMUM_TASKS_LOC")}/Dummy/Dummy_3.json", port = 5000, field = "f")
    f.initialize()
    val result = f(Map("x" -> 1.0, "y" -> 2.0, "z" -> 3.0))
    f.terminate()

    assert(result == 36.0)
    Thread.sleep(5000)

  }

}
