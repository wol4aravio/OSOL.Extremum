package OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions

import spray.json._
import OSOL.Extremum.Cores.JVM.Arithmetics.Interval
import scalaj.http.Http

class IntervalRemoteFunction(override val json: String, override val port: Int, override val field: String)
  extends RemoteFunction[Interval](json, port, field) {

  final override def apply(values: Map[String, Interval]): Interval = {

    val request = Http(s"http://localhost:${this.port}/process_request")
      .param("field", this.field)
      .param("scope", "interval")
      .params(values.map { case (k, v) => (k, v.toJson.toString()) })

    request.asString.body.parseJson.convertTo[Interval]

//    val url = s"http://localhost:${this.port}/process_request?field=${this.field}&scope=interval" + values.map { case (k, v) => s"&$k=${v.toJson}"}.mkString("")
//    val response = scala.io.Source.fromURL(url).mkString.parseJson
//    response.convertTo[Interval]
  }

}