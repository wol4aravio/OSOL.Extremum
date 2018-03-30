package OSOL.Extremum.Core.Scala

package object CodeFeatures {

  implicit class Pipe[I](val x: I) {
    def |>[O](f: I => O): O = f(x)
  }

}
