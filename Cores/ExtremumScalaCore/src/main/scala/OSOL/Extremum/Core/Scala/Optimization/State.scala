package OSOL.Extremum.Core.Scala.Optimization

import scala.reflect.ClassTag

class State[Base, FuncType, V <: Optimizable[Base, FuncType]](var elements: Array[V]) {

  final def apply(id: Int): V = elements(id)

  final def changeElement(id: Int, vNew: V): Unit = {
    this.elements(id) = vNew
  }

  final def <<(id: Int, vNew: V): Unit = this.changeElement(id, vNew)

  final def changeElements(elementsNew: Iterable[V])(implicit c: ClassTag[V]): Unit = {
    this.elements = elementsNew.toArray
  }

}
