package OSOL.Extremum.Core.Scala.Optimization

/** Trait that describes basic requirements for optimizable object
  *
  * @tparam Base type of optimizable object
  */
trait Optimizable[Base] {

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

}