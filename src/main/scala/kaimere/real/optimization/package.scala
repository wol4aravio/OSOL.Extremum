package kaimere.real

import kaimere.real.objects.RealVector
import kaimere.real.objects.Function
import kaimere.tools.random.GoRN

package object optimization {

  object Helper {

    def prepareInitialState(state: Vector[Map[String, Double]]): Vector[RealVector] =
      state.map(x => x.map { case (key, value) => (key, value) }).map(RealVector.fromMap)

    def chooseOneBest(vectors: Vector[RealVector], f: Function): RealVector =
      vectors.map(v => (v, f(v))).minBy(_._2)._1

    def chooseSeveralBest(vectors: Vector[RealVector], f: Function, N: Int): Seq[RealVector] = {
      if (N > vectors.size) {
        val idsChosen = GoRN.getFromSeries(vectors.indices, N, withReturn = true)
        idsChosen.map(vectors(_))
      }
      else vectors.map(v => (v, f(v))).sortBy(_._2).take(N).map(_._1)
    }

  }

}
