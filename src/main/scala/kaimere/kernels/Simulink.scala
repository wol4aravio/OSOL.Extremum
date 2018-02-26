package kaimere.kernels

import kaimere.real.objects.RealVector
import kaimere.real.objects.Function
import spray.json._

object Simulink {

  case class Model(name: String, state: Vector[String], control: Vector[String],
                   criteria: Seq[String], terminalConditions: Seq[String],
                   tunableBlocks: Vector[Blocks.Tunable], parameterArea: Map[String, (Double, Double)],
                   normCoeff: Double = 1.0) extends Function {

    override def apply(v: RealVector): Double = {
      tunableBlocks.foreach(_.tune(v))
      Matlab.eval(s"sim('$name');")

      Matlab.eval("criterion = 0.0;")
      val criteriaValues = criteria.map { criterion =>
        Matlab.eval(s"$criterion = $criterion.Data(end);")
        Matlab.eval(s"criterion = criterion + $criterion;")
        Matlab.getVariable(s"$criterion")
      }

      Matlab.eval("penalty = 0.0;")
      val penalties = terminalConditions.map { terminal =>
        Matlab.eval(s"$terminal = $terminal.Data(end);")
        Matlab.eval(s"penalty = penalty + $terminal;")
        Matlab.getVariable(s"$terminal")
      }

      criteriaValues.sum + penalties.sum
    }

  }

  object Exceptions {

    class UnsupportedBlock(name: String) extends Exception

  }

  object Blocks {

    abstract class Tunable(name: String) {
      def extract(v: RealVector): String
      def tune(v: RealVector): Unit
      def initializeWith(d: Double): Unit
      def prettyPrint(v: RealVector): String = s"$name: ${extract(v)}"
      def toJson(v: RealVector): JsObject = JsObject(
        "name" -> JsString(name),
        "parameters" -> JsString(extract(v)))
    }

    def parseJson(json: JsValue, modelName: String): Tunable = {
      val Seq(JsString(t)) = json.asJsObject.getFields("type")
      t match {
        case "Constant" => {
          val Seq(JsString(n), JsString(v)) = json.asJsObject.getFields("name", "var")
          Simulink.Blocks.Constant(s"$modelName/$n", v)
        }
        case "RepeatingSequenceInterpolated" => {
          val Seq(JsString(n), JsNumber(v)) = json.asJsObject.getFields("name", "numberOfVars")
          Simulink.Blocks.RepeatingSequenceInterpolated(s"$modelName/$n", n, v.toInt)
        }
        case _ => throw new Simulink.Exceptions.UnsupportedBlock(t)
      }
    }

    case class Constant(name: String, parameterName: String) extends Tunable(name) {

      override def extract(v: RealVector): String = {v(parameterName)}.toString

      override def tune(v: RealVector): Unit = Matlab.eval(s"set_param('$name', 'Value', num2str(${extract(v)}))")

      override def initializeWith(d: Double): Unit = Matlab.eval(s"set_param('$name', 'Value', num2str($d))")

    }

    case class RepeatingSequenceInterpolated(name: String, prefix: String, numberOfParameters: Int) extends Tunable(name) {

      override def extract(v: RealVector): String = {
        val selectedVars = Range(0, numberOfParameters).map(key => v(s"${prefix}_${key.toString}"))
        s"[${selectedVars.mkString(", ")}]"
      }

      override def tune(v: RealVector): Unit = Matlab.eval(s"set_param('$name', 'OutValues', '${extract(v)}')")

      override def initializeWith(d: Double): Unit = ???

    }

    case class Gain(name: String) extends Tunable(name) {

      override def extract(v: RealVector): String = ???

      override def tune(v: RealVector): Unit = ???

      override def initializeWith(d: Double): Unit = Matlab.eval(s"set_param('$name', 'Gain', num2str($d))")

    }

    case class DeadZone(name: String) extends Tunable(name) {

      override def extract(v: RealVector): String = ???

      override def tune(v: RealVector): Unit = ???

      override def initializeWith(d: Double): Unit = {
        Matlab.eval(s"set_param('$name', 'LowerValue', num2str(${-d}))")
        Matlab.eval(s"set_param('$name', 'UpperValue', num2str(${+d}))")
      }

    }

  }

}
