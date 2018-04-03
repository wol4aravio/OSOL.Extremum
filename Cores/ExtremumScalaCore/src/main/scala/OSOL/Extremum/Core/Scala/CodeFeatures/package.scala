package OSOL.Extremum.Core.Scala

/** Set of code tools */
package object CodeFeatures {

  /** Pipeline from Haskell */
  implicit class Pipe[I](val x: I) {
    def |>[O](f: I => O): O = f(x)
  }

}
