import org.scoverage.coveralls.Imports.CoverallsKeys._

name := "Kaimere"

version := "0.1"

scalaVersion := "2.11.12"

coverallsTokenFile := Some("../coveralls_token.txt")

coverageMinimum := 95
coverageFailOnMinimum := true