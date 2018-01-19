package kaimere.real.objects

import org.scalatest.FunSuite

import RealVector._

class RealVectorSuite extends FunSuite {

  private val v1 = RealVector("x" -> 1.0, "y" -> 2.0)
  private val v2 = RealVector("x" -> 1.0, "z" -> 2.0)
  private val v3 = RealVector("x" -> 2.0, "y" -> 2.0, "z" -> 2.0)

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

}
