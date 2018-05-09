package OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions

class RealRemoteFunction(override val json: String, override val port: Int, override val field: String)
  extends RemoteFunction[Double](json, port, field) {

  final override def apply(values: Map[String, Double]): Double = {
    val url = s"http://localhost:${this.port}/process_request?field=${this.field}" + values.map { case (k, v) => s"&$k=$v"}.mkString("")
    val response = scala.io.Source.fromURL(url).mkString
    response.toDouble
  }

}
