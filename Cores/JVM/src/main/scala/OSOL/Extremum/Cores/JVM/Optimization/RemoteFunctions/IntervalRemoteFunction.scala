package OSOL.Extremum.Cores.JVM.Optimization.RemoteFunctions

import spray.json._

import OSOL.Extremum.Cores.JVM.Arithmetics.Interval

class IntervalRemoteFunction(override val json: String, override val port: Int, override val field: String)
  extends RemoteFunction[Interval](json, port, field) {

  final override def apply(values: Map[String, Interval]): Interval = {
    val url = s"http://127.0.0.1:${this.port}/process_request?field=${this.field}&scope=interval" + values.map { case (k, v) => s"&$k=${v.toJson}"}.mkString("")
    val response = scala.io.Source.fromURL(url).mkString.parseJson
    response.convertTo[Interval]
  }

}