package kaimere.tools.parser

import sys.process._
import spray.json._

object Parser {

  def parseExpression(function: String, libLoc: String = "libs/parser.py"): JsValue = {
    val json = s"python $libLoc --mode parse --function $function" !!

    JsonParser(json.replace('\'', '\"'))
  }

}