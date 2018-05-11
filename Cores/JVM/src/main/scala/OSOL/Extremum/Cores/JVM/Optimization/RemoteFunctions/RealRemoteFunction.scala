package OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions

import scalaj.http.Http

class RealRemoteFunction(override val json: String, override val port: java.lang.Integer, override val field: String)
  extends RemoteFunction[java.lang.Double](json, port, field) {

  final override def apply(values: Map[String, java.lang.Double]): java.lang.Double = {
    val request = Http(s"http://localhost:${this.port}/process_request")
      .param("field", this.field)
      .params(values.map { case (k, v) => (k, v.toString) })

    java.lang.Double.parseDouble(request.asString.body)
  }

}
