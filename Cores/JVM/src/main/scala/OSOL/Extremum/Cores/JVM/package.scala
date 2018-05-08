package OSOL.Extremum.Cores

package object JVM {

  implicit class Pipe[I](val x: I) {
    def |>[O](f: I => O): O = f(x)
  }

}
