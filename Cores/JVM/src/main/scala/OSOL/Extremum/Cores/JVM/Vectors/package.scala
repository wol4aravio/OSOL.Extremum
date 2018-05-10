package OSOL.Extremum.Cores.JVM

package object Vectors {

  object Exceptions {

    class MissingKeyException(val missingKey: String) extends Exception

    class DifferentKeysException(val keys_1: Set[String], val keys_2: Set[String]) extends Exception

  }

}
