package OSOL.Extremum.Cores.JVM.Optimization

import OSOL.Extremum.Cores.JVM.Vectors.VectorObject
import OSOL.Extremum.Cores.JVM.Vectors.VectorObject
import spray.json.JsValue

trait Optimizable[Base, FuncType] {

  def moveBy(delta: (String, Double)*): Base
  final def moveBy(delta: Iterable[(String, Double)]): Base = this.moveBy(delta.toSeq:_*)

  def constrain(area: (String, (Double, Double))*): Base
  final def constrain(area: Iterable[(String, (Double, Double))]): Base = this.constrain(area.toSeq:_*)

  def getPerformance(f: Map[String, FuncType] => FuncType): Double

  def toBasicForm(): VectorObject[Double]

  def convertToJson(): JsValue

}
