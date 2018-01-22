[![Build Status](https://travis-ci.org/wol4aravio/Kaimere.svg?branch=master)](https://travis-ci.org/wol4aravio/Kaimere.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/wol4aravio/Kaimere/badge.svg?branch=master)](https://coveralls.io/github/wol4aravio/Kaimere?branch=master&service=github)

# Basic Description
Kaimere is project consisting of different optimization algorithms.

# Installation

You should add the following lines to your build.sbt:

```scala
resolvers ++= Seq(
"sonatype snapshots" at "https://oss.sonatype.org/content/repositories/snapshots",
"sonatype releases" at "https://oss.sonatype.org/content/repositories/releases")

libraryDependencies += "com.github.wol4aravio" %% "kaimere" % "0.2.0-SNAPSHOT"
```
