package kaimere.real.optimization.general

import kaimere.real.objects.{RealVector, Function}

case class State(components: Vector[RealVector]) extends Traversable[RealVector] {

  final override def foreach[U](f: RealVector => U): Unit = components.foreach(f)

  final def apply(id: Int): RealVector = components(id)

  final def getBestBy(f: Function): RealVector = this.minBy(x => f(x))

}
