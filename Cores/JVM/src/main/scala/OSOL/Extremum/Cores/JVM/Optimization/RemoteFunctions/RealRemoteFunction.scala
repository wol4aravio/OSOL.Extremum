package OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions

import com.github.kevinsawicki.http.HttpRequest
import scala.collection.JavaConverters

class RealRemoteFunction(override val json: String, override val port: java.lang.Integer, override val field: String)
  extends RemoteFunction[java.lang.Double](json, port, field) {

  final override def apply(values: Map[String, java.lang.Double]): java.lang.Double = {
    val params = Map("field" -> this.field) ++ values.map { case (k, v) => (k, v.toString) }
    val request = HttpRequest.get(s"http://localhost:${this.port}/process_request", JavaConverters.mapAsJavaMap(params), true)

    java.lang.Double.parseDouble(request.body())
  }

}
