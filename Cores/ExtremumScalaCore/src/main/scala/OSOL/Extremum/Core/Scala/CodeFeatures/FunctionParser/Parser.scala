package OSOL.Extremum.Core.Scala.CodeFeatures.FunctionParser

import OSOL.Extremum.Core.Scala.Arithmetics.Interval
import OSOL.Extremum.Core.Scala.CodeFeatures.Pipe

object Parser {

  private object ParserMethods {

    val doubleMinus: (String, String) = "(\\-\\-)" -> "+"
    val plusMinus: (String, String) = "(\\+\\-)" -> "-"
    val minusPlus: (String, String) = "(\\-\\+)" -> "-"
    val inTheBeginning: (String, String) = "(\\A\\-)" -> "~"
    val afterOpeningBracket: (String, String) = "(\\(\\-)" -> "(~"
    val unnecessaryAddition: (String, String) = "(\\(\\+)" -> "("

    val rules = Seq(doubleMinus, plusMinus, minusPlus, inTheBeginning, afterOpeningBracket, unnecessaryAddition)

    val tokenRegex = "(?<=[-+{*}/{)~(}^])|(?=[-+{*}/{)~(}^])"

    val functionNames = Seq("~", "sin", "cos", "exp", "abs", "sqrt", "ln")

    val operators = Seq("+", "-", "*", "/", "^")

    val priority: Map[String, Int] =
      Map(
        "+" -> 1,
        "-" -> 1,
        "*" -> 2,
        "/" -> 2,
        "^" -> 3,
        "(" -> 0,
        ")" -> 0
      ) ++ functionNames.map(_ -> 4)

    val associativity: Map[String, Int] = Map(
      "+" -> -1,
      "-" -> -1,
      "*" -> -1,
      "/" -> -1,
      "^" -> 1
    ) // "-1" for left, "1" for right

    @scala.annotation.tailrec
    def toPostfixPart(seq: Seq[String], stack: Seq[String], postfix: Seq[String]): Seq[String] = seq match {
      case current +: tail =>
        if (functionNames.contains(current) || current == "(") toPostfixPart(tail, current +: stack, postfix)
        else {
          if (current == ")") {
            if (!stack.contains("(")) throw new Exception("Smth is wrong with brackets")
            else {
              val symbols = stack.takeWhile(_ != "(")
              toPostfixPart(tail, stack.drop(symbols.length).tail, postfix ++ symbols)
            }
          }
          else {
            if (operators.contains(current)) {
              val symbols =
                stack.takeWhile { symbol =>
                  (associativity(current) == 1 && priority(symbol) > priority(current)) ||
                    (associativity(current) == -1 && priority(symbol) >= priority(current))
                }
              toPostfixPart(tail, current +: stack.drop(symbols.length), postfix ++ symbols)
            }
            else toPostfixPart(tail, stack, postfix :+ current)
          }
        }
      case Nil =>
        if (!stack.forall(symbol => functionNames.contains(symbol) || operators.contains(symbol)))
          throw new BadBracketsException()
        else
          postfix ++ stack
    }

    @scala.annotation.tailrec
    def buildTreeD(stack: Seq[Tree[Double]], postfix: Seq[String]): Tree[Double] =
      postfix match {
        case current +: rest =>
          current match {
            case "+" => buildTreeD(new TreeD.AdditionTree(stack(1), stack.head) +: stack.drop(2), rest)
            case "-" => buildTreeD(new TreeD.SubtractionTree(stack(1), stack.head) +: stack.drop(2), rest)
            case "*" => buildTreeD(new TreeD.MultiplicationTree(stack(1), stack.head) +: stack.drop(2), rest)
            case "/" => buildTreeD(new TreeD.DivisionTree(stack(1), stack.head) +: stack.drop(2), rest)
            case "^" => buildTreeD(new TreeD.PowerTree(stack(1), stack.head) +: stack.drop(2), rest)
            case "~" => buildTreeD(new TreeD.NegTree(stack.head) +: stack.tail, rest)
            case "sin" => buildTreeD(new TreeD.SinTree(stack.head) +: stack.tail, rest)
            case "cos" => buildTreeD(new TreeD.CosTree(stack.head) +: stack.tail, rest)
            case "exp" => buildTreeD(new TreeD.ExpTree(stack.head) +: stack.tail, rest)
            case "abs" => buildTreeD(new TreeD.AbsTree(stack.head) +: stack.tail, rest)
            case "ln" => buildTreeD(new TreeD.LnTree(stack.head) +: stack.tail, rest)
            case "sqrt" => buildTreeD(new TreeD.SqrtTree(stack.head) +: stack.tail, rest)
            case varName if current.matches("[a-zA-z]{1,}\\d{0,}") => buildTreeD(new TreeD.VariableTree(varName) +: stack, rest)
            case _ => buildTreeD(new TreeD.ConstantTree(current.toDouble) +: stack, rest)
          }
        case Nil => stack.head
      }

    @scala.annotation.tailrec
    def buildTreeI(stack: Seq[Tree[Interval]], postfix: Seq[String]): Tree[Interval] =
      postfix match {
        case current +: rest =>
          current match {
            case "+" => buildTreeI(new TreeI.AdditionTree(stack(1), stack.head) +: stack.drop(2), rest)
            case "-" => buildTreeI(new TreeI.SubtractionTree(stack(1), stack.head) +: stack.drop(2), rest)
            case "*" => buildTreeI(new TreeI.MultiplicationTree(stack(1), stack.head) +: stack.drop(2), rest)
            case "/" => buildTreeI(new TreeI.DivisionTree(stack(1), stack.head) +: stack.drop(2), rest)
            case "^" => buildTreeI(new TreeI.PowerTree(stack(1), stack.head) +: stack.drop(2), rest)
            case "~" => buildTreeI(new TreeI.NegTree(stack.head) +: stack.tail, rest)
            case "sin" => buildTreeI(new TreeI.SinTree(stack.head) +: stack.tail, rest)
            case "cos" => buildTreeI(new TreeI.CosTree(stack.head) +: stack.tail, rest)
            case "exp" => buildTreeI(new TreeI.ExpTree(stack.head) +: stack.tail, rest)
            case "abs" => buildTreeI(new TreeI.AbsTree(stack.head) +: stack.tail, rest)
            case "ln" => buildTreeI(new TreeI.LnTree(stack.head) +: stack.tail, rest)
            case "sqrt" => buildTreeI(new TreeI.SqrtTree(stack.head) +: stack.tail, rest)
            case varName if current.matches("[a-zA-z]{1,}\\d{0,}") => buildTreeI(new TreeI.VariableTree(varName) +: stack, rest)
            case _ => buildTreeI(new TreeI.ConstantTree(Interval(current.toDouble)) +: stack, rest)
          }
        case Nil => stack.head
      }

    def prepare(str: String): String =
      rules.foldLeft(str) { case (s, (rule, sub)) => s.replaceAll(rule, sub) }

    def toTokens(str: String): Seq[String] =
      str.split(tokenRegex)

    def toPostfix(seq: Seq[String]): Seq[String] =
      toPostfixPart(seq, Seq(), Seq())

    def toTreeD(postfix: Seq[String]): Tree[Double] =
      buildTreeD(Seq(), postfix)

    def toTreeI(postfix: Seq[String]): Tree[Interval] =
      buildTreeI(Seq(), postfix)

  }

  def parseToDoubleTree(str: String): Tree[Double] =
    str |> ParserMethods.prepare |> ParserMethods.toTokens |> ParserMethods.toPostfix |> ParserMethods.toTreeD

  def parseToIntervalTree(str: String): Tree[Interval] =
    str |> ParserMethods.prepare |> ParserMethods.toTokens |> ParserMethods.toPostfix |> ParserMethods.toTreeI

}