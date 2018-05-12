package OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions

import spray.json._
import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import com.github.kevinsawicki.http.HttpRequest

import scala.collection.JavaConverters

class IntervalRemoteFunction(override val json: String, override val port: java.lang.Integer, override val field: String)
  extends RemoteFunction[Interval](json, port, field) {

  final override def apply(values: Map[String, Interval]): Interval = {
    val params = Map("field" -> this.field, "scope" -> "interval") ++ values.map { case (k, v) => (k, v.toJson.toString) }
    val request = HttpRequest.get(s"http://localhost:${this.port}/process_request", JavaConverters.mapAsJavaMap(params), true)

    request.body().parseJson.convertTo[Interval]
  }

}