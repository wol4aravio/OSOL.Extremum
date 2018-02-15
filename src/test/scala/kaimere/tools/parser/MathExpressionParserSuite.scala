package kaimere.tools.parser

import spray.json._
import org.scalatest.FunSuite

class MathExpressionParserSuite extends FunSuite {

  val f1: String = "x ** 2 - 3 * (-y)"
  val f2: String = "x ** x"
  val f3: String = "sin(x - y - z)"
  val f4: String = "cond(leq(x, 2), x, x ** 2)"

  ignore("Expression String Parser #1") {

    val parsed = MathExpressionParser.parseExpression(f1)

    val json = JsObject(
      "type" -> JsString("binary"),
      "op" -> JsString("sub"),
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

    assert(parsed == json)
  }

  ignore("Expression String Parser #2") {

    val parsed = MathExpressionParser.parseExpression(f2)

    val json = JsObject(
      "type" -> JsString("binary"),
      "op" -> JsString("pow"),
      "left" -> JsObject(
        "type" -> JsString("var"),
        "name" -> JsString("x")
      ),
      "right" -> JsObject(
        "type" -> JsString("var"),
        "name" -> JsString("x")
      )
    )

    assert(parsed == json)
  }

  ignore("Expression String Parser #3") {

    val parsed = MathExpressionParser.parseExpression(f3)

    val json = JsObject(
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
              "type" -> JsString("var"),
              "name" -> JsString("x")
            ),
            "right" -> JsObject(
              "type" -> JsString("var"),
              "name" -> JsString("y")
            )
          ),
          "right" -> JsObject(
            "type" -> JsString("var"),
            "name" -> JsString("z")
          )
        )
      )
    )

    assert(parsed == json)
  }

  ignore("Expression String Parser #4") {

    val parsed = MathExpressionParser.parseExpression(f4)

    val json = JsObject(
      "type" -> JsString("func"),
      "func" -> JsString("cond"),
      "args" -> JsArray(
        JsObject(
          "type" -> JsString("func"),
          "func" -> JsString("leq"),
          "args" -> JsArray(
            JsObject(
              "type" -> JsString("var"),
              "name" -> JsString("x")
            ),
            JsObject(
              "type" -> JsString("const"),
              "value" -> JsNumber(2)
            )
          )
        ),
        JsObject(
          "type" -> JsString("var"),
          "name" -> JsString("x")
        ),
        JsObject(
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
        )
      )
    )

    assert(parsed == json)
  }

}
