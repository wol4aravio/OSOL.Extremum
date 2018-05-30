name := "OSOL.Extremum.Apps.JVM.Runner"

assemblyJarName in assembly := "OSOL.Extremum.Apps.JVM.Runner.jar"

version := "0.1.0"

scalaVersion := "2.12.5"

resolvers ++= Seq(
  "sonatype snapshots" at "https://oss.sonatype.org/content/repositories/snapshots",
  "sonatype releases" at "https://oss.sonatype.org/content/repositories/releases")

libraryDependencies += "org.rogach" %% "scallop" % "3.1.1"

libraryDependencies += "com.github.wol4aravio" %% "OSOL.Extremum.Cores.JVM" % "0.0.5.1-SNAPSHOT"
libraryDependencies += "com.github.wol4aravio" %% "OSOL.Extremum.Algorithms.Scala.RandomSearch" % "0.0.5.2-SNAPSHOT"
libraryDependencies += "com.github.wol4aravio" %% "OSOL.Extremum.Algorithms.Scala.IntervalExplosionSearch" % "0.0.5.1-SNAPSHOT"
libraryDependencies += "com.github.wol4aravio" % "OSOL.Extremum.Algorithms.Java.RandomSearch_1.8" % "0.0.5.1-SNAPSHOT"
