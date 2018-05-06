package OSOL.Extremum.Cores.JVM.Vectors

import org.scalatest.FunSuite
import spray.json._

import OSOL.Extremum.Cores.JVM.Vectors.RealVector.Converters._
import OSOL.Extremum.Cores.JVM.Vectors.Exceptions._
import OSOL.Extremum.Cores.JVM.Pipe

class RealVectorSuite extends FunSuite {

  val v1: RealVector = Map("x" -> 1.0, "y" -> 2.0, "z" -> 3.0)
  val v2: RealVector = Map("x" -> -1.0, "y" -> -2.0, "z" -> -3.0)
  val v3: RealVector = Map("x" -> -1.0, "z" -> -3.0)
  val z: RealVector = Map("x" -> 0.0, "y" -> 0.0, "z" -> 0.0)

  test("Keys") {
    assert(v1.keys == Set("x", "y", "z"))
  }

  test("Value Extraction") {

    assert(v1("x") == 1.0)
    assert(v1("y") == 2.0)
    assert(v1("z", 0.0) == 3.0)
    assert(v1("a", 0.0) == 0.0)
    intercept[MissingKeyException] { v1("a") }

  }

  test("To String") {
    assert(v1.toString == "x -> 1.0\ny -> 2.0\nz -> 3.0")
  }

  test("Addition") {
    assert(v1 + v2 == z)
    intercept[DifferentKeysException] { v1 + v3 }
  }

  test("Addition with Imputation") {
    assert(v1 ~+ v3 == (Map("x" -> 0.0, "y" -> 2.0, "z" -> 0.0) |> RealVector.apply))
  }

  test("Subtraction") {
    assert(z - v1 == v2)
    intercept[DifferentKeysException] { v1 - v3 }
  }

  test("Subtraction with Imputation") {
    assert(v1 ~- v3 == (Map("x" -> 2.0, "y" -> 2.0, "z" -> 6.0) |> RealVector.apply))
  }

  test("Multiplication") {
    assert(v1 * v1 == v2 * v2)
    assert(v1 * v2 == -v1 * v1)
    intercept[DifferentKeysException] { v1 * v3 }

  }

  test("Multiplication with Imputation") {
    assert(v1 ~* v3 == (Map("x" -> -1.0, "y" -> 2.0, "z" -> -9.0) |> RealVector.apply))
  }

  test("Multiply by coefficient") {
    assert(v1 + v1 == v1 * 2.0)
  }

  test("Move by") {
    assert(v1.moveBy("x" -> -1.0).moveBy(Seq("z" -> -3.0, "y" -> -2.0)) == z)
  }

  test("Constraining") {
    assert(v1
      .constrain("x" -> (-1.0, 0.0))
      .constrain(Seq("y" -> (3.0, 10.0)))
      .constrain("z" -> (-5.0, 5.0)) == (Map("x" -> 0.0, "y" -> 3.0, "z" -> 3.0) |> RealVector.apply))
  }

  test("Get Performance") {
    val f: Map[String, Double] => Double = v => v("x") + v("y") + v("z")
    assert(v1.getPerformance(f) == 6.0)
    assert((v1 * 2.0).getPerformance(f) == 12.0)
  }

  test("To Double Valued Vector") {
    assert(v1.toBasicForm()("x") == 1.0)
    assert(v1.toBasicForm()("y") == 2.0)
    assert(v1.toBasicForm()("z") == 3.0)
  }

  test("Union") {
    val p1: RealVector = Map("x" -> 1.0)
    val p2 = "y" -> 2.0
    val p3 = "z" -> 3.0
    assert(p1.union(p2, p3) == v1)
  }

  test("Distance from Area") {
    val area = Map("x" -> (Double.NegativeInfinity, 0.0), "y" -> (Double.NegativeInfinity, Double.PositiveInfinity), "z" -> (2.5, 2.7))
    val distances = v1.distanceFromArea(area)
    val tol = 1e-9
    assert(math.abs(distances("x") - 1.0) < tol)
    assert(math.abs(distances("y") - 0.0) < tol)
    assert(math.abs(distances("z") - 0.3) < tol)
  }

  test("JSON") {
    assert(v1.convertToJson.convertTo[RealVector] == v1)
    assert(v2.convertToJson.convertTo[RealVector] == v2)
    intercept[DeserializationException]
      { v1.convertToJson.prettyPrint.replace("RealVector", "Vector").parseJson.convertTo[RealVector]}
    intercept[DeserializationException]
      { v1.convertToJson.prettyPrint.replace("elements", "values").parseJson.convertTo[RealVector]}
    intercept[DeserializationException]
      { v1.convertToJson.prettyPrint.replace("key", "k").parseJson.convertTo[RealVector]}
    intercept[DeserializationException]
      { v1.convertToJson.prettyPrint.replace("value", "v").parseJson.convertTo[RealVector]}
  }

}