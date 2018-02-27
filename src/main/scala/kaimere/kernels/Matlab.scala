package kaimere.kernels

import java.io.File
import java.lang.reflect.Method
import java.net.{URL, URLClassLoader}
import java.nio.file.{Path, Paths}

import kaimere.kernels.Simulink.Blocks.Tunable
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

  def getTimeSeries(name: String): (Seq[Double], Seq[Double]) = {
    this.eval(s"t_ = $name.Time;")
    this.eval(s"v_ = $name.Data;")
    val time: Seq[Double] = getVariable.invoke(engine, "t_").asInstanceOf[Array[Double]]
    val values: Seq[Double] = getVariable.invoke(engine, "v_").asInstanceOf[Array[Double]]
    (time, values)
  }

  def initializeBlocks(json: JsValue, modelName: String): Unit = {
    val Seq(JsString(name), JsString(parameter), JsString(value)) = json.asJsObject.getFields("name", "parameter", "value")
    Matlab.eval(s"set_param('$modelName/$name', '$parameter', '$value')")
  }

  def loadSimulinkModel(model: String, jsonConfig: String): Simulink.Model  = {
    val json = scala.io.Source.fromFile(jsonConfig).mkString.parseJson.asJsObject
    val Seq(
    JsString(name),
    JsArray(stateJson),
    JsArray(controlJson),
    JsArray(criteria),
    JsArray(terminalConditions),
    JsArray(initializationJsons),
    JsArray(tunableJson),
    JsArray(parameters)) =
      json.getFields("name", "state", "control", "criteria", "terminalConditions", "initialization", "tunable", "parameters")

    val state = stateJson.map(_.asInstanceOf[JsString].value)
    val control = controlJson.map(_.asInstanceOf[JsString].value)

    val blocks = tunableJson.map(Simulink.Blocks.parseJson(_, name))

    val area = parameters.map {
      case part =>
        val Seq(JsArray(vars), JsNumber(min), JsNumber(max)) = part.asJsObject.getFields("vars", "min", "max")
        vars.map{ case JsString(varName) => (varName, (min.toDouble, max.toDouble))}
    }.map { _.toMap[String, (Double, Double)]}.reduce(_ ++ _)

    val path = Paths.get(model).toAbsolutePath.toString
    eval(s"load_system('$path')")

    initializationJsons.foreach(initializeBlocks(_, name))

    Simulink.Model(
      name, state, control,
      criteria.map(_.asInstanceOf[JsString].value),
      terminalConditions.map(_.asInstanceOf[JsString].value), blocks, area)

  }

  def unloadSimulinkModel(model: String): Unit = {
    eval(s"save_system('$model')")
    eval(s"close_system('$model')")
  }

}
