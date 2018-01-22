package kaimere.tools

package object random {

  def getProbability[T](values: Seq[T], project: T => Int): Map[Int, Double] = {
    val valuesProjected = values.map(project)
    valuesProjected
      .distinct
      .map { value => (value, valuesProjected.filter(_ == value).length.toDouble / valuesProjected.length) }
      .toMap
  }

  implicit class OverloadedMap[T](val v: Map[T, Double]) {
    def ~(that: OverloadedMap[T]): Double = {
      val keys = (this.v.keys ++ that.v.keys).toSeq.distinct
      keys
        .map { key =>
          val v1 = this.v.getOrElse(key, 0.0)
          val v2 = that.v.getOrElse(key, 0.0)
          math.abs(v1 - v2)
        }.sum / keys.length
    }
  }

}