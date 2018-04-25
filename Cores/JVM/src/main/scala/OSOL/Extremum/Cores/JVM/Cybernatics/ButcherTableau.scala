package OSOL.Extremum.Cores.JVM.Cybernatics

case class ButcherTableau(a: Map[(Int, Int), Double], b: Map[Int, Double], c: Map[Int, Double]) {

  def numberOfParts = b.size

  def getA(i: Int, j: Int): Double = a.getOrElse((i, j), 0.0)

  def getB(i: Int): Double = b.getOrElse(i, 0.0)

  def getC(i: Int): Double = c.getOrElse(i, 0.0)

}

object ButcherTableau {

  def getEuler: ButcherTableau =
    ButcherTableau(
      a = Map(),
      b = Map(1 -> 1.0),
      c = Map())

  def getRK4: ButcherTableau =
    ButcherTableau(
      a = Map((2, 1) -> 0.5, (3, 2) -> 0.5, (4, 3) -> 1.0),
      b = Map(1 -> 1.0 / 6.0, 2 -> 1.0 / 3.0, 3 -> 1.0 / 3.0, 4 -> 1.0 / 6.0),
      c = Map(2 -> 0.5, 3 -> 0.5, 4 -> 1.0))

}