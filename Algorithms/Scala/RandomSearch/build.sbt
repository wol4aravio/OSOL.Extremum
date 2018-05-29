name := "OSOL.Extremum.Algorithms.Scala.RandomSearch"

version := "0.0.5.2"

scalaVersion := "2.12.5"

libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.5" % "test"

resolvers ++= Seq(
  "sonatype snapshots" at "https://oss.sonatype.org/content/repositories/snapshots",
  "sonatype releases" at "https://oss.sonatype.org/content/repositories/releases")

libraryDependencies += "com.github.wol4aravio" %% "OSOL.Extremum.Cores.JVM" % "0.0.5.1-SNAPSHOT"
