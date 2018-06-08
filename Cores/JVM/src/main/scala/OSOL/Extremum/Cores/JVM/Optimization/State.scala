package OSOL.Extremum.Cores.JVM.Optimization

import OSOL.Extremum.Cores.JVM.Optimization.Exceptions._
import spray.json._
import spray.json.DefaultJsonProtocol._

class State[Base, FuncType, V <: Optimizable[Base, FuncType]] {

  var result: Option[V] = None

  final private val parameters: scala.collection.mutable.Map[String, Any] = scala.collection.mutable.Map.empty[String, Any]

  def setParameter[T <: Any](name: String, value: T): Unit = parameters(name) = value

  def getParameter[T <: Any](name: String): T = {
    if (parameters.contains(name)) parameters(name).asInstanceOf[T]
    else throw new NoSuchParameterException(name)
  }

  def toJson(writers: Seq[Any => JsValue]): JsValue = {
    JsObject(
      "result" -> {
        if (result.isDefined) result.get.convertToJson() else JsString("None")
      },
      "parameters" -> JsArray(parameters.map { case (k, v) => JsObject(k -> {
        v match {
          case b: java.lang.Boolean => JsBoolean(b)
          case b: Boolean => JsBoolean(b)
          case d: java.lang.Double => JsNumber(d)
          case d: Double => JsNumber(d)
          case i: java.lang.Integer => JsNumber(i)
          case i: Int => JsNumber(i)
          case l: java.lang.Long => JsNumber(l)
          case l: Long => JsNumber(l)
          case m: Map[String, java.lang.Double] =>
            JsArray(m.map { case (key, value) => JsObject("key" -> JsString(key), "value" -> JsNumber(value)) }.toVector)
          case m: Map[String, Double] =>
            JsArray(m.map { case (key, value) => JsObject("key" -> JsString(key), "value" -> JsNumber(value)) }.toVector)
          case _ => {
            try {
              v.asInstanceOf[V].convertToJson()
            }
            catch {
              case e: Exception => {
                try {
                  JsArray(v.asInstanceOf[Traversable[V]].map(_.convertToJson()).toVector)
                }
                catch {
                  case e: Exception => {
                    try {
                      val writerResluts = writers.map { w =>
                        try { Some(w(v)) }
                        catch { case _: Exception => None }
                      }
                      if (writerResluts.length > 0) writerResluts.filter(_.isDefined).head.get
                      else throw new Exception(s"Can't serialize ($k, $v)")
                    }
                    catch {
                      case e: Exception => throw new Exception(s"Can't serialize ($k, $v)")
                    }
                  }
                }
              }
            }
          }
        }
      })
      }.toVector)
    )
  }

}