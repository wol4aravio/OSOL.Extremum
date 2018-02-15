package kaimere.tools.parser

import sys.process._
import spray.json._

object MathExpressionParser {

  def parseExpression(function: String): JsValue = {

    val libLoc = getClass.getResource("/parser.py").getFile
    val json = s"python $libLoc --mode parse --function $function" !!

    JsonParser(json.replace('\'', '\"'))
  }

}