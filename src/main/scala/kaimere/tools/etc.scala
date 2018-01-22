package kaimere.tools

object etc {

  implicit class Pipe[I](val x: I) {
    def |>[O](f: I => O): O = f(x)
  }

}
