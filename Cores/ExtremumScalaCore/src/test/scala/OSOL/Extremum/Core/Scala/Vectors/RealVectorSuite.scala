package OSOL.Extremum.Core.Scala.Vectors

import org.scalatest.FunSuite

import OSOL.Extremum.Core.Scala.Vectors.RealVector.Converters._
import OSOL.Extremum.Core.Scala.CodeFeatures.Pipe

class RealVectorSuite extends FunSuite {

  val v1: RealVector = Map("x" -> 1.0, "y" -> 2.0, "z" -> 3.0)
  val v2: RealVector = Map("x" -> -1.0, "y" -> -2.0, "z" -> -3.0)
  val v3: RealVector = Map("x" -> -1.0, "z" -> -3.0)
  val z: RealVector = Map("x" -> 0.0, "y" -> 0.0, "z" -> 0.0)

  test("Keys") {
    assert(v1.keys == Set("x", "y", "z"))
  }

  test("Values") {
    assert(v1.values.toSeq == Seq(1.0, 2.0, 3.0))
  }

  test("Value Extraction") {

    assert(v1("x") == 1.0)
    assert(v1("y") == 2.0)
    assert(v1("z", 0.0) == 3.0)
    assert(v1("a", 0.0) == 0.0)

  }

  test("To String") {
    assert(v1.toString == "x -> 1.0\ny -> 2.0\nz -> 3.0")
  }

  test("Addition") {
    assert(v1 + v2 == z)
    assert(v1 + v1 == v1 * 2.0)
  }

  test("Addition with Imputation") {
    assert(v1 ~+ v3 == (Map("x" -> 0.0, "y" -> 2.0, "z" -> 0.0) |> RealVector.apply))
  }



}
