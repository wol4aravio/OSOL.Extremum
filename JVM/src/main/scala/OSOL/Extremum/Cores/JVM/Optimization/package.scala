package OSOL.Extremum.Cores.JVM

/** Set of optimization tools */
package object Optimization {

  /** Area alias */
  type Area = Map[String, (Double, Double)]

  /** Possible exceptions for `Optimization` */
  object Exceptions {

    /** Exception arises when parameter is already included during initialization phase
      *
      * @param parameterName parameter name
      */
    class ParameterAlreadyExistsException(parameterName: String) extends Exception

    /** Exception arises when accessing parameter does not exist in `State`
      *
      * @param parameterName parameter name
      */
    class NoSuchParameterException(parameterName: String) extends Exception

  }

}
