name := "RandomSearch"

version := "0.0.1"

scalaVersion := "2.12.5"

resolvers ++= Seq(
  "sonatype snapshots" at "https://oss.sonatype.org/content/repositories/snapshots",
  "sonatype releases" at "https://oss.sonatype.org/content/repositories/releases")

libraryDependencies += "com.github.wol4aravio" %% "OSOL.Extremum.ScalaCore" % "0.0.3-SNAPSHOT"