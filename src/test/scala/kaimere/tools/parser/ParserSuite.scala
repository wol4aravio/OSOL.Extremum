package kaimere.tools.parser

import spray.json._
import org.scalatest.FunSuite

class ParserSuite extends FunSuite {

  val f1: String = "x**2-3*(-y)"
  val f2: String = "x**x"
  val f3: String = "sin(x-y-z)"

  test("Expression String Parser") {

    val parsed_1 = Parser.parseExpression(f1)
    val parsed_2 = Parser.parseExpression(f2)
    val parsed_3 = Parser.parseExpression(f3)

    val json_1 = JsObject(
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
    val json_2 = JsObject(
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

    assert(parsed_1 == json_1)
    assert(parsed_2 == json_2)
    assert(parsed_3 == json_3)
  }

}
