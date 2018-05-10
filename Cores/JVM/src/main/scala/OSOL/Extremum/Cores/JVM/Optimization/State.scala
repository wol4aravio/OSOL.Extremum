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

  def toJson(): JsValue = {
    JsObject(
      "result" -> {
        if (result.isDefined) result.get.convertToJson() else JsString("None")
      },
      "parameters" -> JsArray(parameters.map { case (k, v) => JsObject(k -> {
        v match {
          case b: Boolean => JsBoolean(b)
          case d: Double => JsNumber(d)
          case i: Int => JsNumber(i)
          case l: Long => JsNumber(l)
          case _ => {
            try {v.asInstanceOf[V].convertToJson()}
            catch {
              case e: Exception => {
                try { JsArray(v.asInstanceOf[Traversable[V]].map(_.convertToJson()).toVector) }
                catch {
                  case e: Exception => throw new Exception(s"Can't serialize ($k, $v)")
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