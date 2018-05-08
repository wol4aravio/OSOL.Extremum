package OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions

//import scala.sys.process.Process

abstract class RemoteFunction[FuncType](val json: String, val port: Int, val field: String) {

  val process_specs = Array("run_core", "--core", json, "--port", port.toString)
  var server_process: Process = null
  var pid = -1

  def initialize(): Unit = {
    server_process = Runtime.getRuntime.exec(process_specs)
    val f = server_process.getClass.getDeclaredField("pid");
    f.setAccessible(true)
    pid = f.getInt(server_process)

    Thread.sleep(5000)
  }

  def apply(values: Map[String, FuncType]): FuncType

  def terminate(): Unit = {
    try
      {
        Runtime.getRuntime.exec(s"kill -9 $pid")
      }
    catch {
      case _: Exception => Runtime.getRuntime.exec(s"taskkill /F /PID $pid")
    }
  }

}
