package OSOL.Extremum.Core.Scala.Optimization

import OSOL.Extremum.Core.Scala.Vectors.VectorObject
import spray.json.JsValue

/** Trait that describes basic requirements for optimizable object
  *
  * @tparam Base type of optimizable object
  * @tparam FuncType required function type
  */
trait Optimizable[Base, FuncType] {

  /** Moves current object
    *
    * @param delta shift per key
    * @return moved object
    */
  def moveBy(delta: (String, Double)*): Base
  /** Same as `moveBy(delta: (String, Double)*)` */
  final def moveBy(delta: Iterable[(String, Double)]): Base = this.moveBy(delta.toSeq:_*)

  /** Forces object to be located in given area
    *
    * @param area area where object must be located
    * @return object in target area
    */
  def constrain(area: (String, (Double, Double))*): Base
  /** Same as `constrain(area: (String, (Double, Double))*)` */
  final def constrain(area: Iterable[(String, (Double, Double))]): Base = this.constrain(area.toSeq:_*)

  /** How to measure efficiency on target function
    *
    * @param f target function
    * @return fitness value (lower - better)
    */
  def getPerformance(f: Map[String, FuncType] => FuncType): Double

  /** Converts current object to a form that can be used somewhere else */
  def toBasicForm(): VectorObject[Double]

  /** Converts to JSON */
  def convertToJson(): JsValue

}
