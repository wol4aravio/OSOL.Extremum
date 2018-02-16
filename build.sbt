import org.scoverage.coveralls.Imports.CoverallsKeys._

name := "Kaimere"

version := "0.5.0.0"

scalaVersion := "2.11.12"

resolvers += "spray repo" at "http://repo.spray.io"

val sprayVersion = "1.3.4"
libraryDependencies += "io.spray" %% "spray-json" % sprayVersion

libraryDependencies += "org.scalactic" %% "scalactic" % "3.0.4"
libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.4" % "test"

coverallsTokenFile := Some("../coveralls_token.txt")