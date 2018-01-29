import org.scoverage.coveralls.Imports.CoverallsKeys._

name := "Kaimere"

version := "0.4.1"

scalaVersion := "2.11.12"

resolvers += "spray repo" at "http://repo.spray.io"

val sprayVersion = "1.3.4"
libraryDependencies += "io.spray" %% "spray-json" % sprayVersion

libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.4"

coverallsTokenFile := Some("../coveralls_token.txt")