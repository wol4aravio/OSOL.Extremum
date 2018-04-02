package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Optimization.Exceptions._

import scala.reflect.ClassTag

class State[Base, FuncType, V <: Optimizable[Base, FuncType]](var elements: Array[V]) {

  final lazy val capacity = elements.length

  final def apply(id: Int): V = elements(id)

  final def changeElement(id: Int, vNew: V): Unit = {
    this.elements(id) = vNew
  }

  final def <<(id: Int, vNew: V): Unit = this.changeElement(id, vNew)

  final def changeElements(elementsNew: Iterable[V])(implicit c: ClassTag[V]): Unit = {
    this.elements = elementsNew.toArray
  }

  final private val parameters: scala.collection.mutable.Map[String, Any] = scala.collection.mutable.Map.empty[String, Any]

  def setParameter[T <: Any](name: String, value: T): Unit = parameters(name) = value

  def getParameter[T <: Any](name: String): T = {
    if (parameters.contains(name)) parameters(name).asInstanceOf[T]
    else throw new NoSuchParameterException(name)
  }

}
