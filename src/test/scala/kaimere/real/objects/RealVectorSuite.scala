package kaimere.real.objects

import org.scalatest.FunSuite

import RealVector._

class RealVectorSuite extends FunSuite {

  private val v_1 = RealVector("x" -> 1.0, "y" -> 2.0)
  private val v_2 = RealVector("x" -> 1.0, "z" -> 2.0)
  private val v_3 = RealVector("x" -> 2.0, "y" -> 2.0, "z" -> 2.0)

  test("Keys") {

    val targetKeys = Set("x", "y", "z")
    val keys_v3 = v_3.keys.toSet
    val keySet_v3 = v_3.keySet

    assert(targetKeys == keys_v3)
    assert(targetKeys == keySet_v3)

  }

}
