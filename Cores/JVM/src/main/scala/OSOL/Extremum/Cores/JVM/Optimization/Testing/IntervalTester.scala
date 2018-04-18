package OSOL.Extremum.Cores.JVM.Optimization.Testing

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.Arithmetics.Interval.Converters._
import OSOL.Extremum.Cores.JVM.Optimization.Area
import OSOL.Extremum.Cores.JVM.Vectors.IntervalVector

class IntervalTester extends Tester[IntervalVector, Interval, IntervalVector](
  testFunctions = IntervalTester.f,
  areas = IntervalTester.a,
  solutions = IntervalTester.s,
  tolerance = IntervalTester.tolerance,
  attempts = IntervalTester.attempts) {

}

object IntervalTester {

  val tolerance = 1e-3
  val attempts = 5

  val vars_1 = Seq("x")
  val vars_2 = Seq("x", "y")
  val vars_3 = Seq("x", "y", "z")


  val f1: Map[String, Interval] => Interval = (v: Map[String, Interval]) => v("x").pow(2.0)
  val a1: Area = vars_1.map(k => (k, (-10.0, 10.0))).toMap
  val s1: Map[String, Double] = vars_1.map(k => (k, 0.0)).toMap

  val f2: Map[String, Interval] => Interval = (v: Map[String, Interval]) => v("x").pow(2.0) + v("y").pow(2.0)
  val a2: Area = vars_2.map(k => (k, (-10.0, 10.0))).toMap
  val s2: Map[String, Double] = vars_2.map(k => (k, 0.0)).toMap

  val f3: Map[String, Interval] => Interval = (v: Map[String, Interval]) => v("x").pow(2.0) + v("y").pow(2.0) + v("z").pow(2.0)
  val a3: Area = vars_3.map(k => (k, (-10.0, 10.0))).toMap
  val s3: Map[String, Double] = vars_3.map(k => (k, 0.0)).toMap


  val f = Seq(f1, f2, f3)
  val a = Seq(a1, a2, a3)
  val s = Seq(s1, s2, s3)

}