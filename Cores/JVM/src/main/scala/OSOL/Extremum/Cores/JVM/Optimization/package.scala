package OSOL.Extremum.Cores.JVM

package object Optimization {

  type Area = Map[String, (java.lang.Double, java.lang.Double)]

  implicit def pureScalaArea(area: Map[String, (Double, Double)]): Area =
    area.mapValues { case (a, b) => (new java.lang.Double(a), new java.lang.Double(b))}

  object Exceptions {

    class ParameterAlreadyExistsException(parameterName: String) extends Exception

    class NoSuchParameterException(parameterName: String) extends Exception

  }

}
