package OSOL.Extremum.Cores.JVM.Optimization.Testing

import OSOL.Extremum.Cores.JVM.Optimization.Area
import OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions.RealRemoteFunction
import OSOL.Extremum.Cores.JVM.Vectors.RealVector

class RealTester extends Tester[RealVector, Double, RealVector](
  testFunctions = RealTester.f,
  areas = RealTester.a,
  solutions = RealTester.s,
  tolerance = RealTester.tolerance,
  attempts = RealTester.attempts) {

}

object RealTester {

  val tolerance = 1e-3
  val attempts = 5

  val vars_1 = Seq("x")
  val vars_2 = Seq("x", "y")
  val vars_3 = Seq("x", "y", "z")

  val TASKS_LOC = sys.env("OSOL_EXTREMUM_TASKS_LOC")

  val f1: RealRemoteFunction = new RealRemoteFunction(json = s"${TASKS_LOC}/Dummy/Dummy_1.json", port = 11001, field = "f")
  val a1: Area = vars_1.map(k => (k, (-10.0, 10.0))).toMap
  val s1: Map[String, Double] = vars_1.map(k => (k, 0.0)).toMap

  val f2: RealRemoteFunction = new RealRemoteFunction(json = s"${TASKS_LOC}/Dummy/Dummy_2.json", port = 11002, field = "f")
  val a2: Area = vars_2.map(k => (k, (-10.0, 10.0))).toMap
  val s2: Map[String, Double] = vars_2.map(k => (k, 0.0)).toMap

  val f3: RealRemoteFunction = new RealRemoteFunction(json = s"${TASKS_LOC}/Dummy/Dummy_3.json", port = 11003, field = "f")
  val a3: Area = vars_3.map(k => (k, (-10.0, 10.0))).toMap
  val s3: Map[String, Double] = vars_3.map(k => (k, 0.0)).toMap


  val f = Seq(f1, f2, f3)
  val a = Seq(a1, a2, a3)
  val s = Seq(s1, s2, s3)

}