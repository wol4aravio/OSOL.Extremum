package kaimere.real.objects

import org.scalatest.FunSuite

import RealVector._
import RealVector.Exceptions._

import spray.json._

class RealVectorSuite extends FunSuite {

  private val v1: RealVector = Map("x" -> 1.0, "y" -> 2.0)
  private val v2: RealVector = Map("x" -> 1.0, "z" -> 2.0)
  private val v3: RealVector = Map("x" -> 2.0, "y" -> 2.0, "z" -> 2.0)
  private val v4: RealVector = Map("x" -> -1.0, "y" -> -2.0)

  test("JSON") {
    val json = "{ \"keys\": [\"x\", \"y\", \"z\"], \"values\": [1.0, 2.0, 3.0]}".parseJson
    assert(RealVector("x" -> 1.0, "y" -> 2.0, "z" -> 3.0) == json.convertTo[RealVector])
  }

  test("Keys") {
    val targetKeys = Set("x", "y", "z")
    val keys_v3 = v3.keys.toSet
    val keySet_v3 = v3.keySet

    assert(targetKeys == keys_v3)
    assert(targetKeys == keySet_v3)
  }

  test("Values") {
    val targetValues = Seq(1.0, 2.0)
    val values_v1 = v1.values
    assert(targetValues.zip(values_v1).forall { case (left, right) => left == right})
  }

  test("Application") {
    assert(v2("x") == 1.0)
  }

  test("GetOrElse") {
    assert(v1.getOrElse("x", 0.0) == 1.0)
    assert(v1.getOrElse("z", 0.0) == 0.0)
  }

  test("Strict Addition") {
    assert(v1 + v4 == RealVector("x" -> 0.0, "y" -> 0.0))
    val success =
      try { val _ = v1 + v2; true}
      catch {
        case _: DifferentKeysException => true
        case _: Throwable => false
      }
    assert(success)
  }

  test("NonStrict Addition") {
    assert(v1 ~+ v4 == RealVector("x" -> 0.0, "y" -> 0.0))
    assert(v1 ~+ v2 == v3)
  }

  test("Multiplication by Coefficient") {
    assert(v1 * 2 == RealVector("x" -> 2.0, "y" -> 4.0))
    assert(v2 * 2 == RealVector("x" -> 2.0, "z" -> 4.0))
    assert(v3 * 2 == RealVector("x" -> 4.0, "y" -> 4.0, "z" -> 4.0))
  }

  test("Negation") {
    assert(-v1 == RealVector("x" -> -1.0, "y" -> -2.0))
    assert(-v3 == RealVector("x" -> -2.0, "y" -> -2.0, "z" -> -2.0))
  }

  test("Strict Difference") {
    assert(v1 - v4 == RealVector("x" -> 2.0, "y" -> 4.0))
    val success =
      try { val _ = v1 - v2; true}
      catch {
        case _: DifferentKeysException => true
        case _ : Throwable => false
      }
    assert(success)
  }

  test("NonStrict Difference") {
    assert(v1 ~- v4 == RealVector("x" -> 2.0, "y" -> 4.0))
    assert(v1 ~- v2 == RealVector("x" -> 0.0, "y" -> 2.0, "z" -> -2.0))
  }

  test("Move by") {
    val delta_1 = Map("x" -> -1.0)
    val delta_2 = Map("y" -> -2.0, "z" -> -2.0)
    assert(v1.moveBy(delta_1) == RealVector("x" -> 0.0, "y" -> 2.0))
    assert(v3.moveBy(delta_2) == RealVector("x" -> 2.0, "y" -> 0.0, "z" -> 0.0))
  }

  test("Constraining #1") {
    val area = Map("x" -> (-1.0, 0.5), "z" -> (3.0, 4.0))
    val constrained = v3.constrain(area)
    assert(constrained == RealVector("x" -> 0.5, "y" -> 2.0, "z" -> 3.0))
  }

  test("Constraining #2") {
    val area = Map("x" -> (-3.0, 0.5), "y" -> (0.0, 10.0), "z" -> (3.0, 4.0))
    val constrained = v3.constrain(area)
    assert(constrained == RealVector("x" -> 0.5, "y" -> 2.0, "z" -> 3.0))
  }


}
