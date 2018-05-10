package OSOL.Extremum.Cores.JVM.Optimization

import OSOL.Extremum.Cores.JVM.Vectors.VectorObject
import OSOL.Extremum.Cores.JVM.Vectors.VectorObject
import spray.json.JsValue

trait Optimizable[Base, FuncType] {

  def moveBy(delta: (String, java.lang.Double)*): Base
  final def moveBy(delta: Iterable[(String, java.lang.Double)]): Base = this.moveBy(delta.toSeq:_*)

  def constrain(area: (String, (java.lang.Double, java.lang.Double))*): Base
  final def constrain(area: Iterable[(String, (java.lang.Double, java.lang.Double))]): Base = this.constrain(area.toSeq:_*)

  def getPerformance(f: Map[String, FuncType] => FuncType): java.lang.Double

  def toBasicForm(): VectorObject[java.lang.Double]

  def convertToJson(): JsValue



  final def moveByScala(delta: (String, Double)*): Base =
    this.moveBy(delta.map { case (k, v) => (k, new java.lang.Double(v)) })
  final def moveByScala(delta: Iterable[(String, Double)]): Base =
    this.moveByScala(delta.toSeq:_*)

  final def constrainScala(area: (String, (Double, Double))*): Base =
    this.constrain(area.map { case (k, (a, b)) => (k, (new java.lang.Double(a), new java.lang.Double(b))) })
  final def constrainScala(area: Iterable[(String, (Double, Double))]): Base = this.constrainScala(area.toSeq:_*)



}
