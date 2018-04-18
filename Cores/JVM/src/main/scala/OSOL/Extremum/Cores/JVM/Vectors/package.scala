package OSOL.Extremum.Cores.JVM

/** Set of tools and procedures for VectorObjects package */
package object Vectors {

  /** Exceptions that can be invoked by [[OSOL.Extremum.Cores.JVM.Vectors.VectorObject VectorObject]] class
    *
    */
  object Exceptions {

    /** Accessed key is  not present in current VectorObject
      *
      * @param missingKey key that is not present in current VectorObject
      */
    class MissingKeyException(val missingKey: String) extends Exception

    /** Performed operation required objects to have the same keys
      *
      * @param keys_1 first object keys
      * @param keys_2 second object keys
      */
    class DifferentKeysException(val keys_1: Set[String], val keys_2: Set[String]) extends Exception

  }

}