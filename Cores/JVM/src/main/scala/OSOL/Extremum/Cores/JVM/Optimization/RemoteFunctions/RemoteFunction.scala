package OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions

import scala.sys.process.Process

abstract class RemoteFunction[FuncType](val json: String, val port: Int, val field: String) {

  val process_specs = Process("run_core", Seq("--core", json, "--port", port.toString))
  var server_process: Process = null

  def initialize(): Unit = {
    server_process = process_specs.run()
    Thread.sleep(RemoteFunction.INIT_TIME * 1000)
  }

  def apply(values: Map[String, FuncType]): FuncType

  def terminate(): Unit = {
    server_process.destroy()
  }

}

object RemoteFunction {

  val INIT_TIME = sys.env("OSOL_EXTREMUM_SERVER_INIT_TIME").toInt

}