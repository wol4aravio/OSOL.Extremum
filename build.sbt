import org.scoverage.coveralls.Imports.CoverallsKeys._

name := "Kaimere"

version := "0.1"

scalaVersion := "2.11.12"

libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.4"

coverallsTokenFile := Some("../coveralls_token.txt")
coverageMinimum := 95
coverageFailOnMinimum := true