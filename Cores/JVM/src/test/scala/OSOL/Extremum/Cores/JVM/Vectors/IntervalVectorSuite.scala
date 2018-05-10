package OSOL.Extremum.Cores.JVM.Vectors

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import org.scalatest.FunSuite
import OSOL.Extremum.Cores.JVM.Vectors.IntervalVector.Converters._
import OSOL.Extremum.Cores.JVM.Vectors.Exceptions._
import OSOL.Extremum.Cores.JVM.Pipe
import spray.json._

class IntervalVectorSuite extends FunSuite {

  val v1: IntervalVector = Map("x" -> Interval(1.0), "y" -> Interval(2.0, 3.0), "z" -> Interval(3.0, 5.0))
  val v2: IntervalVector = Map("x" -> Interval(1.0), "z" -> Interval(-3.0, -2.0))

  test("Keys") {
    assert(v1.keys == Set("x", "y", "z"))
  }

  test("Value Extraction") {

    assert(v1("x") == Interval(1.0))
    assert(v1("y") == Interval(2.0, 3.0))
    assert(v1("z", Interval(0.0)) == Interval(3.0, 5.0))
    assert(v1("a", Interval(0.0)) == Interval(0.0))
    intercept[MissingKeyException] { v1("a") }

  }

  test("To String") {
    assert(v1.toString == "x -> [1.0; 1.0]\ny -> [2.0; 3.0]\nz -> [3.0; 5.0]")
  }

  test("Addition") {
    assert(v1 + v1 == v1 * 2.0)
    intercept[DifferentKeysException] { v1 + v2 }
  }

  test("Addition with Imputation") {
    assert(v1 ~+ v2 == (Map("x" -> Interval(2.0), "y" -> v1("y"), "z" -> Interval(0.0, 3.0)) |> IntervalVector.apply))
  }

  test("Subtraction") {
    assert(v1 - v1 == (Map("x" -> Interval(0.0), "y" -> Interval(-1.0, 1.0), "z" -> Interval(-2.0, 2.0)) |> IntervalVector.apply))
    intercept[DifferentKeysException] { v1 - v2 }
  }

  test("Subtraction with Imputation") {
    assert(v1 ~- v2 == (Map("x" -> Interval(0.0), "y" -> v1("y"), "z" -> Interval(5.0, 8.0)) |> IntervalVector.apply))
  }

  test("Multiplication") {
    assert(v1 * v1 == (Map("x" -> Interval(1.0), "y" -> Interval(4.0, 9.0), "z" -> Interval(9.0, 25.0)) |> IntervalVector.apply))
    intercept[DifferentKeysException] { v1 * v2 }

  }

  test("Multiplication with Imputation") {
    assert(v1 ~* v2 == (Map("x" -> Interval(1.0), "y" -> Interval(2.0, 3.0), "z" -> Interval(-15.0, -6.0)) |> IntervalVector.apply))
  }

  test("Multiply by coefficient") {
    assert(v1 + v1 == v1 * 2.0)
  }

  test("Move by") {
    assert(v1.moveBy("x" -> -1.0).moveBy(Seq("z" -> -3.0, "y" -> -2.0)) == (Map("x" -> Interval(0.0), "y" -> Interval(0.0, 1.0), "z" -> Interval(0.0, 2.0)) |> IntervalVector.apply))
  }

  test("Constraining") {
    assert(v1
      .constrain("x" -> (-1.0, 0.0))
      .constrain(Seq("y" -> (3.0, 10.0)))
      .constrain("z" -> (-5.0, 4.0)) == (Map("x" -> Interval(0.0), "y" -> Interval(3.0), "z" -> Interval(3.0, 4.0)) |> IntervalVector.apply))
  }

  test("To Double Valued Vector") {
    assert(v1.toBasicForm()("x") == 1.0)
    assert(v1.toBasicForm()("y") == 2.5)
    assert(v1.toBasicForm()("z") == 4.0)
  }

  test("Splitting # 1") {
    val (left, right) = v1.bisect()
    assert(left == (Map("x" -> Interval(1.0), "y" -> Interval(2.0, 3.0), "z" -> Interval(3.0, 4.0)) |> IntervalVector.apply))
    assert(right == (Map("x" -> Interval(1.0), "y" -> Interval(2.0, 3.0), "z" -> Interval(4.0, 5.0)) |> IntervalVector.apply))
  }

  test("Splitting # 2") {
    val (left, right) = v1.bisect(key = Some("y"))
    assert(left == (Map("x" -> Interval(1.0), "y" -> Interval(2.0, 2.5), "z" -> Interval(3.0, 5.0)) |> IntervalVector.apply))
    assert(right == (Map("x" -> Interval(1.0), "y" -> Interval(2.5, 3.0), "z" -> Interval(3.0, 5.0)) |> IntervalVector.apply))
  }

  test("Union") {
    val p1: IntervalVector = Map("x" -> Interval(1.0))
    val p2 = "y" -> Interval(2.0, 3.0)
    val p3 = "z" -> Interval(3.0, 5.0)
    assert(p1.union(p2, p3) == v1)
  }

  test("Distance from Area") {
    val area = Map("x" -> (Double.NegativeInfinity, 0.0), "y" -> (Double.NegativeInfinity, Double.PositiveInfinity), "z" -> (2.5, 2.7))
    val distances = v1.distanceFromArea(area)
    val tol = 1e-9
    assert(math.abs(distances("x") - 1.0) < tol)
    assert(math.abs(distances("y") - 0.0) < tol)
    assert(math.abs(distances("z") - 2.3) < tol)
  }

  test("JSON") {
    assert(v1.convertToJson.convertTo[IntervalVector] == v1)
    assert(v2.convertToJson.convertTo[IntervalVector] == v2)
    intercept[DeserializationException]
      { v1.convertToJson.prettyPrint.replace("IntervalVector", "Vector").parseJson.convertTo[IntervalVector]}
    intercept[DeserializationException]
      { v1.convertToJson.prettyPrint.replace("elements", "values").parseJson.convertTo[IntervalVector]}
    intercept[DeserializationException]
      { v1.convertToJson.prettyPrint.replace("key", "k").parseJson.convertTo[IntervalVector]}
    intercept[DeserializationException]
      { v1.convertToJson.prettyPrint.replace("value", "v").parseJson.convertTo[IntervalVector]}
  }

}