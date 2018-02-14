package kaimere.real.objects.tree_function

import kaimere.real.objects.{RealVector, Function}

import spray.json._

class TreeFunction private(val expression: Tree) extends Function {

  override def apply(vector: RealVector): Double = expression.eval(vector)

}

object TreeFunction {

  private def parse(json: JsValue): Tree = {
    val jsonObject = json.asJsObject
    jsonObject.getFields("type") match {
      case Seq(JsString("binary")) => {
        val Seq(op, left, right) = jsonObject.getFields("op", "left", "right")
        val leftTree = parse(left)
        val rightTree = parse(right)
        op match {
          case JsString("add") => new Tree.AdditionTree(leftTree, rightTree)
          case JsString("sub") => new Tree.SubtractionTree(leftTree, rightTree)
          case JsString("mult") => new Tree.MultiplicationTree(leftTree, rightTree)
          case JsString("div") => new Tree.DivisionTree(leftTree, rightTree)
          case JsString("pow") => new Tree.PowerTree(leftTree, rightTree)
          case _ => throw new Exception(s"Unsupported op: $op")
        }
      }
      case Seq(JsString("unary")) => {
        val Seq(op, operand) = jsonObject.getFields("op", "operand")
        val operandTree = parse(operand)
        op match {
          case JsString("usub") => new Tree.NegTree(operandTree)
          case _ => throw new Exception(s"Unsupported op: $op")
        }
      }
      case Seq(JsString("func")) => {
        val Seq(func, args) = jsonObject.getFields("func", "args")
        val argsTrees = args.asInstanceOf[JsArray].elements.map(parse)
        func match {
          case JsString("sin") => new Tree.SinTree(argsTrees(0))
          case JsString("cos") => new Tree.CosTree(argsTrees(0))
          case JsString("exp") => new Tree.ExpTree(argsTrees(0))
          case JsString("abs") => new Tree.AbsTree(argsTrees(0))
          case JsString("sign") => new Tree.SignTree(argsTrees(0))
          case JsString("ln") => new Tree.LnTree(argsTrees(0))
          case JsString("sqrt") => new Tree.SqrtTree(argsTrees(0))
          case JsString("leq") => new Tree.LeqTree(argsTrees(0), argsTrees(1))
          case JsString("eq") => new Tree.EqTree(argsTrees(0), argsTrees(1))
          case JsString("cond") => new Tree.CondTree(argsTrees(0), argsTrees(1), argsTrees(2))
          case _ => throw new Exception(s"Unsupported func: $func")
        }
      }
      case Seq(JsString("const")) => {
        val Seq(value) = jsonObject.getFields("value")
        new Tree.ConstantTree(value.toString().toDouble)
      }
      case Seq(JsString("var")) => {
        val Seq(name) = jsonObject.getFields("name")
        new Tree.VariableTree(name.toString().drop(1).dropRight(1))
      }
      case _ => throw new Exception(s"Can't parse $json")
    }
  }

  def apply(json: JsValue): TreeFunction =
    new TreeFunction(parse(json))

}