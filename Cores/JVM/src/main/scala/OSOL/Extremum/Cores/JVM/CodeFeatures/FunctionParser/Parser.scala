package OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser

import java.io.{File, PrintWriter}

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser.Trees.{Tree, TreeD, TreeI}
import OSOL.Extremum.Cores.JVM.CodeFeatures._
import OSOL.Extremum.Cores.JVM.CodeFeatures.FunctionParser.Trees.{Tree, TreeI}
import spray.json._

import scala.sys.process.Process

object Parser {
  
  class UnsupportedOperation(message: String) extends Exception

  def buildTreeD(json: JsValue): Tree[Double] = {
    val jsonObject = json.asJsObject
    jsonObject.getFields("type") match {
      case Seq(JsString("binary")) => {
        val Seq(op, left, right) = jsonObject.getFields("op", "left", "right")
        val leftTree = buildTreeD(left)
        val rightTree = buildTreeD(right)
        op match {
          case JsString("add") => new TreeD.AdditionTree(leftTree, rightTree)
          case JsString("sub") => new TreeD.SubtractionTree(leftTree, rightTree)
          case JsString("mult") => new TreeD.MultiplicationTree(leftTree, rightTree)
          case JsString("div") => new TreeD.DivisionTree(leftTree, rightTree)
          case JsString("pow") => new TreeD.PowerTree(leftTree, rightTree)
          case _ => throw new UnsupportedOperation(s"Unsupported op: $op")
        }
      }
      case Seq(JsString("unary")) => {
        val Seq(op, operand) = jsonObject.getFields("op", "operand")
        val operandTree = buildTreeD(operand)
        op match {
          case JsString("usub") => new TreeD.NegTree(operandTree)
          case _ => throw new UnsupportedOperation(s"Unsupported op: $op")
        }
      }
      case Seq(JsString("func")) => {
        val Seq(func, args) = jsonObject.getFields("func", "args")
        val argsTrees = args.asInstanceOf[JsArray].elements.map(buildTreeD)
        func match {
          case JsString("sin") => new TreeD.SinTree(argsTrees(0))
          case JsString("cos") => new TreeD.CosTree(argsTrees(0))
          case JsString("exp") => new TreeD.ExpTree(argsTrees(0))
          case JsString("abs") => new TreeD.AbsTree(argsTrees(0))
          case JsString("ln") => new TreeD.LnTree(argsTrees(0))
          case JsString("sqrt") => new TreeD.SqrtTree(argsTrees(0))
          case _ => throw new UnsupportedOperation(s"Unsupported func: $func")
        }
      }
      case Seq(JsString("const")) => {
        val Seq(value) = jsonObject.getFields("value")
        new TreeD.ConstantTree(value.toString().toDouble)
      }
      case Seq(JsString("var")) => {
        val Seq(name) = jsonObject.getFields("name")
        new TreeD.VariableTree(name.toString().drop(1).dropRight(1))
      }
      case _ => throw new DeserializationException(s"Can't parse $json")
    }
  }

  def buildTreeI(json: JsValue): Tree[Interval] = {
    val jsonObject = json.asJsObject
    jsonObject.getFields("type") match {
      case Seq(JsString("binary")) => {
        val Seq(op, left, right) = jsonObject.getFields("op", "left", "right")
        val leftTree = buildTreeI(left)
        val rightTree = buildTreeI(right)
        op match {
          case JsString("add") => new TreeI.AdditionTree(leftTree, rightTree)
          case JsString("sub") => new TreeI.SubtractionTree(leftTree, rightTree)
          case JsString("mult") => new TreeI.MultiplicationTree(leftTree, rightTree)
          case JsString("div") => new TreeI.DivisionTree(leftTree, rightTree)
          case JsString("pow") => new TreeI.PowerTree(leftTree, rightTree)
          case _ => throw new UnsupportedOperation(s"Unsupported op: $op")
        }
      }
      case Seq(JsString("unary")) => {
        val Seq(op, operand) = jsonObject.getFields("op", "operand")
        val operandTree = buildTreeI(operand)
        op match {
          case JsString("usub") => new TreeI.NegTree(operandTree)
          case _ => throw new UnsupportedOperation(s"Unsupported op: $op")
        }
      }
      case Seq(JsString("func")) => {
        val Seq(func, args) = jsonObject.getFields("func", "args")
        val argsTrees = args.asInstanceOf[JsArray].elements.map(buildTreeI)
        func match {
          case JsString("sin") => new TreeI.SinTree(argsTrees(0))
          case JsString("cos") => new TreeI.CosTree(argsTrees(0))
          case JsString("exp") => new TreeI.ExpTree(argsTrees(0))
          case JsString("abs") => new TreeI.AbsTree(argsTrees(0))
          case JsString("ln") => new TreeI.LnTree(argsTrees(0))
          case JsString("sqrt") => new TreeI.SqrtTree(argsTrees(0))
          case _ => throw new UnsupportedOperation(s"Unsupported func: $func")
        }
      }
      case Seq(JsString("const")) => {
        val Seq(value) = jsonObject.getFields("value")
        new TreeI.ConstantTree(Interval(value.toString().toDouble))
      }
      case Seq(JsString("var")) => {
        val Seq(name) = jsonObject.getFields("name")
        new TreeI.VariableTree(name.toString().drop(1).dropRight(1))
      }
      case _ => throw new DeserializationException(s"Can't parse $json")
    }
  }

  def parseString(str: String): JsValue = {
    val rootFolder = "temp"
    val parserLibFile = extractResource("parser", "py", "parser", s"$rootFolder/parser")
    val parserLibInitFile = extractResource("__init__", "py", "parser", s"$rootFolder/parser")
    val parserAppFile = extractResource("parser_app", "py", "apps", s"$rootFolder")
    val treeJson = (Process("python",  Seq(parserAppFile.getAbsolutePath, "--function", str)) !!)
      .replace('\'', '\"')
      .replace("u\"", "\"")
      .parseJson
    deleteDirectory(new File(rootFolder))
    treeJson
  }

  def parseToDoubleTree(str: String): Tree[Double] = str |> parseString |> buildTreeD

  def parseToIntervalTree(str: String): Tree[Interval] = str |> parseString |> buildTreeI
}