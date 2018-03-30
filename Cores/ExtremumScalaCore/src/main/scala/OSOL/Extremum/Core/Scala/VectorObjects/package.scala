package OSOL.Extremum.Core.Scala

/** Set of tools and procedures for VectorObjects package
  *
  */
package object VectorObjects {

  /** Exceptions that can be invoked by [[OSOL.Extremum.Core.Scala.VectorObjects.VectorObject VectorObject]] class
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
