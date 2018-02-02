[![Build Status](https://travis-ci.org/wol4aravio/Kaimere.svg?branch=master&pony=1)](https://travis-ci.org/wol4aravio/Kaimere.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/wol4aravio/Kaimere/badge.svg?branch=master&pony=1)](https://coveralls.io/github/wol4aravio/Kaimere?branch=master&service=github)

# Basic Description
Kaimere is project consisting of different optimization algorithms.

# Installation

You should add the following lines to your build.sbt:

```scala
resolvers ++= Seq(
"sonatype snapshots" at "https://oss.sonatype.org/content/repositories/snapshots",
"sonatype releases" at "https://oss.sonatype.org/content/repositories/releases")

libraryDependencies += "com.github.wol4aravio" %% "kaimere" % "0.3.3-SNAPSHOT"
```
# Current Status
Given version includes the following optimization algorithms:
* [Random Search](https://en.wikipedia.org/wiki/Random_search)
* [Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing)
* [Cat Swarm Optimization](https://www.researchgate.net/publication/221419703_Cat_Swarm_Optimization)

# Usage Instructions
Target function must extend `Function` trait:
```scala
class DummyFunction(f: Map[String, Double] => Double) extends Function {
  override def apply(vector: RealVector): Double = f(vector.vals)
}
val f = new DummyFunction((v: Map[String, Double]) => v("x") * v("x"))
```

Then you specialize search area:
```scala
val area: OptimizationAlgorithm.Area = Map("x" -> (-10.0, 10.0))
```

Next you create optimization algorithm providing all neccessary parameters:
```scala
val RS = RandomSearch(numberOfAttempts = 10, deltaRatio = 0.01)
```

After all previous steps you can initialize your algorithm with chosen starting sets of points and merge strategy:
```scala
tool.initialize(f, area, state = null, mergeStrategy = MergeStrategy.selfInit)
```

Finally, result can be obtained calling the `work` procedure provided with appropriate `instruction`
```scala
val result = tool.work(instruction)
```

# Instructions
Current version supports to type of instructions:
* `MaxIterations` - this instruction terminates algorithm according to maximum allowed number of iterations,
* `MaxTime` - this instruction terminates algorithm according to maximum allowed working time. 

# Merge Strategies
* `force` - forces algorithm to use provided set of points as a base for algorithm,
* `selfInit` - algorithm randomly initializes its initial state.
