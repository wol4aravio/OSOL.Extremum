package kaimere.kernels

import java.io.File
import java.lang.reflect.Method
import java.net.{URL, URLClassLoader}
import java.nio.file.{Path, Paths}

import spray.json._
import kaimere.real.objects.RealVector

object Matlab {

  private var initialized: Boolean = false

  private var engine: Object = null

  private var start: Method = null
  private var close: Method = null
  private var eval: Method = null
  private var getVariable: Method = null

  def initialize(engineLocation: String): Unit = {
    val jarFile = new File(engineLocation)
    val myClassLoader = new URLClassLoader(Array[URL](jarFile.toURL()))
    val engineClass = myClassLoader.loadClass("com.mathworks.engine.MatlabEngine")

    Matlab.start = engineClass.getMethod("startMatlab")
    Matlab.close = engineClass.getMethod("close")
    Matlab.eval = engineClass.getMethod("eval", classOf[String])
    Matlab.getVariable = engineClass.getMethod("getVariable", classOf[String])

    Matlab.engine = Matlab.start.invoke(null)
    Matlab.initialized = true
  }

  def terminate(): Unit = {
    if (Matlab.initialized) {
      Matlab.close.invoke(Matlab.engine)
      Matlab.initialized = false
    }
  }

  def eval(command: String): Unit =
    eval.invoke(engine, command)

  def getVariable(name: String): Double = {
    getVariable.invoke(engine, name).asInstanceOf[Double]
  }

  def loadSimulinkModel(model: String, jsonConfig: String): Simulink.Model  = {
    val json = scala.io.Source.fromFile(jsonConfig).mkString.parseJson.asJsObject
    val Seq(
    JsString(name),
    JsArray(stateJson),
    JsArray(controlJson),
    JsString(criterionIntegral),
    JsString(criterionTerminal),
    JsArray(terminalConditionJson),
    JsArray(tunableJson)) =
      json.getFields("name", "state", "control", "criterionIntegral", "criterionTerminal", "terminalCondition", "tunable")

    val state = stateJson.map(_.asInstanceOf[JsString].value)
    val control = controlJson.map(_.asInstanceOf[JsString].value)

    val terminalCondition = terminalConditionJson.map { j =>
      val Seq(JsString(terminalName), JsNumber(terminalValue), JsNumber(terminalPenalty), JsNumber(terminalTolerance)) =
        j.asJsObject.getFields("name", "value", "penalty", "tolerance")
      (terminalName, terminalValue.toDouble, terminalPenalty.toDouble, terminalTolerance.toDouble)
    }

    val blocks = tunableJson
      .map { j =>
        val Seq(JsString(t)) = j.asJsObject.getFields("type")
        t match {
          case "Constant" => {
            val Seq(JsString(n), JsString(v)) = j.asJsObject.getFields("name", "var")
            Simulink.Blocks.Constant(s"$name/$n", v)
          }
          case "RepeatingSequenceInterpolated" => {
            val Seq(JsString(n), JsNumber(v)) = j.asJsObject.getFields("name", "numberOfVars")
            Simulink.Blocks.RepeatingSequenceInterpolated(s"$name/$n", n, v.toInt)
          }
          case _ => throw new Simulink.Exceptions.UnsupportedBlock(t)
        }
      }

    val path = Paths.get(model).toAbsolutePath().toString()
    eval(s"load_system('$path')")
    Simulink.Model(name, state, control, criterionIntegral, criterionTerminal, terminalCondition, blocks)
  }

  def unloadSimulinkModel(model: String): Unit = {
    eval(s"save_system('$model')")
    eval(s"close_system('$model')")
  }

}
