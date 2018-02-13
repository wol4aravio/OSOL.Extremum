package kaimere.real.objects.tree_function

import kaimere.real.objects.{RealVector, Function}

import scala.math._
import org.scalatest.FunSuite
import spray.json._

class TreeFunctionsSuite extends FunSuite {

  val funcReal_1: RealVector => Double = (v: RealVector) => pow(v("x"), 2.0) + 3.0 * (-v("y"))
  val funcReal_2: RealVector => Double = (v: RealVector) => exp(v("x")) / log(v("x"))
  val funcReal_3: RealVector => Double = (v: RealVector) => sin(cos(v("x"))-abs(v("y"))-sqrt(v("z")))

  val realVector_1: RealVector = Map("x" -> 1.0, "y" -> 2.0, "z" -> 3.0)
  val realVector_2: RealVector = Map("x" -> 3.0, "y" -> -5.0, "z" -> 1.0)
  val realVector_3: RealVector = Map("x" -> 2.0, "y" -> 0.0, "z" -> 2.0)

  val json_1 = JsObject(
    "type" -> JsString("binary"),
    "op" -> JsString("add"),
    "left" -> JsObject(
      "type" -> JsString("binary"),
      "op" -> JsString("pow"),
      "left" -> JsObject(
        "type" -> JsString("var"),
        "name" -> JsString("x")
      ),
      "right" -> JsObject(
        "type" -> JsString("const"),
        "value" -> JsNumber(2)
      )
    ),
    "right" -> JsObject(
      "type" -> JsString("binary"),
      "op" -> JsString("mult"),
      "left" -> JsObject(
        "type" -> JsString("const"),
        "value" -> JsNumber(3)
      ),
      "right" -> JsObject(
        "type" -> JsString("unary"),
        "op" -> JsString("usub"),
        "operand" -> JsObject(
          "type" -> JsString("var"),
          "name" -> JsString("y")
        )
      )
    )
  )
  val json_2 = JsObject(
    "type" -> JsString("binary"),
    "op" -> JsString("div"),
    "left" -> JsObject(
      "type" -> JsString("func"),
      "func" -> JsString("exp"),
      "args" -> JsArray(
        JsObject(
          "type" -> JsString("var"),
          "name" -> JsString("x")
        )
      )
    ),
    "right" -> JsObject(
      "type" -> JsString("func"),
      "func" -> JsString("ln"),
      "args" -> JsArray(
        JsObject(
          "type" -> JsString("var"),
          "name" -> JsString("x")
        )
      )
    )
  )
  val json_3 = JsObject(
    "type" -> JsString("func"),
    "func" -> JsString("sin"),
    "args" -> JsArray(
      JsObject(
        "type" -> JsString("binary"),
        "op" -> JsString("sub"),
        "left" -> JsObject(
          "type" -> JsString("binary"),
          "op" -> JsString("sub"),
          "left" -> JsObject(
            "type" -> JsString("func"),
            "func" -> JsString("cos"),
            "args" -> JsArray(
              JsObject(
                "type" -> JsString("var"),
                "name" -> JsString("x")
              )
            )
          ),
          "right" -> JsObject(
            "type" -> JsString("func"),
            "func" -> JsString("abs"),
            "args" -> JsArray(
              JsObject(
                "type" -> JsString("var"),
                "name" -> JsString("y")
              )
            )
          )
        ),
        "right" -> JsObject(
          "type" -> JsString("func"),
          "func" -> JsString("sqrt"),
          "args" -> JsArray(
            JsObject(
              "type" -> JsString("var"),
              "name" -> JsString("z")
            )
          )
        )
      )
    )
  )

  val jsonBad_1 = JsObject(
    "type" -> JsString("binary"),
    "op" -> JsString("addition"),
    "left" -> JsObject(
      "type" -> JsString("binary"),
      "op" -> JsString("pow"),
      "left" -> JsObject(
        "type" -> JsString("var"),
        "name" -> JsString("x")
      ),
      "right" -> JsObject(
        "type" -> JsString("const"),
        "value" -> JsNumber(2)
      )
    ),
    "right" -> JsObject(
      "type" -> JsString("binary"),
      "op" -> JsString("mult"),
      "left" -> JsObject(
        "type" -> JsString("const"),
        "value" -> JsNumber(3)
      ),
      "right" -> JsObject(
        "type" -> JsString("unary"),
        "op" -> JsString("usub"),
        "operand" -> JsObject(
          "type" -> JsString("var"),
          "name" -> JsString("y")
        )
      )
    )
  )
  val jsonBad_2 = JsObject(
    "type" -> JsString("binary"),
    "op" -> JsString("add"),
    "left" -> JsObject(
      "type" -> JsString("binary"),
      "op" -> JsString("pow"),
      "left" -> JsObject(
        "type" -> JsString("var"),
        "name" -> JsString("x")
      ),
      "right" -> JsObject(
        "type" -> JsString("const"),
        "value" -> JsNumber(2)
      )
    ),
    "right" -> JsObject(
      "type" -> JsString("binary"),
      "op" -> JsString("mult"),
      "left" -> JsObject(
        "type" -> JsString("const"),
        "value" -> JsNumber(3)
      ),
      "right" -> JsObject(
        "type" -> JsString("unary"),
        "op" -> JsString("uadd"),
        "operand" -> JsObject(
          "type" -> JsString("var"),
          "name" -> JsString("y")
        )
      )
    )
  )
  val jsonBad_3 = JsObject(
    "type" -> JsString("binary"),
    "op" -> JsString("div"),
    "left" -> JsObject(
      "type" -> JsString("func"),
      "func" -> JsString("exponent"),
      "args" -> JsArray(
        JsObject(
          "type" -> JsString("var"),
          "name" -> JsString("x")
        )
      )
    ),
    "right" -> JsObject(
      "type" -> JsString("func"),
      "func" -> JsString("ln"),
      "args" -> JsArray(
        JsObject(
          "type" -> JsString("var"),
          "name" -> JsString("x")
        )
      )
    )
  )
  val jsonBad_4 = JsObject(
    "type" -> JsString("unknown"),
    "value" -> JsString("NA")
  )

  test("Bad JSONs") {
    assert(
      try { val func = TreeFunction(jsonBad_1); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
    assert(
      try { val func = TreeFunction(jsonBad_2); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
    assert(
      try { val func = TreeFunction(jsonBad_3); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
    assert(
      try { val func = TreeFunction(jsonBad_4); false }
      catch {
        case _: Exception => true
        case _: Throwable => false
      })
  }

  test("Function Calc") {

    val realFunction_1 = TreeFunction(json_1)
    val realFunction_2 = TreeFunction(json_2)
    val realFunction_3 = TreeFunction(json_3)

    assert(realFunction_1(realVector_1) == funcReal_1(realVector_1))
    assert(realFunction_1(realVector_2) == funcReal_1(realVector_2))
    assert(realFunction_1(realVector_3) == funcReal_1(realVector_3))

    assert(realFunction_2(realVector_1) == funcReal_2(realVector_1))
    assert(realFunction_2(realVector_2) == funcReal_2(realVector_2))
    assert(realFunction_2(realVector_3) == funcReal_2(realVector_3))

    assert(realFunction_3(realVector_1) == funcReal_3(realVector_1))
    assert(realFunction_3(realVector_2) == funcReal_3(realVector_2))
    assert(realFunction_3(realVector_3) == funcReal_3(realVector_3))

  }

}
