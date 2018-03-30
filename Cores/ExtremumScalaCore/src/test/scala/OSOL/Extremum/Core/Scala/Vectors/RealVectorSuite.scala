package OSOL.Extremum.Core.Scala.Vectors

import org.scalatest.FunSuite

import OSOL.Extremum.Core.Scala.Vectors.RealVector.Converters._

class RealVectorSuite extends FunSuite {

  val v1: RealVector = Map("x" -> 1.0, "y" -> 2.0, "z" -> 3.0)

  test("Value Extraction") {

    assert(v1("x") == 1.0)
    assert(v1("y") == 2.0)
    assert(v1("z") == 3.0)

  }

}
