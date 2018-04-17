name := "ExtremumScalaCore"

version := "0.0.2"

scalaVersion := "2.12.5"

libraryDependencies += "io.spray" %%  "spray-json" % "1.3.3"
libraryDependencies += "org.scalactic" %% "scalactic" % "3.0.5"
libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.5" % "test"

resourceDirectory in Compile := baseDirectory.value.getParentFile.getParentFile / "PyTools"
resourceDirectory in Test := baseDirectory.value.getParentFile.getParentFile / "PyTools"