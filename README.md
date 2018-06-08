[![Build Status](https://travis-ci.org/wol4aravio/OSOL.Extremum.svg?branch=master)](https://travis-ci.org/wol4aravio/OSOL.Extremum.svg?branch=master)
[![codecov](https://codecov.io/gh/wol4aravio/OSOL.Extremum/branch/master/graph/badge.svg)](https://codecov.io/gh/wol4aravio/OSOL.Extremum)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6d29733e0b2d4faea9b99306ecff0f91)](https://www.codacy.com/app/wol4aravio/OSOL.Extremum?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wol4aravio/OSOL.Extremum&amp;utm_campaign=Badge_Grade)

<p align="center">
<b> Open-Source Optimization Library - Extremum </b>
</p>

<p align="justify">
Optimization theory is a widely-used field of mathematics that can be applied to different tasks: pure engineering problems (e.g., obtaining optimal wing shape), control synthesis tasks (e.g., determination of optimal guidance of aircraft), and even machine learning (e.g., training procedures of neural networks). Currently mostly all applied software systems support optimization procedures in a very limited form. This fact leads to several problems: black-box effect (i.e., there is no opportunity to explore source code, modify it, or simply verify), no code reuse (i.e., implemented procedures are accessible only within software that includes it), limitation of modern optimization algorithm application (i.e., number of optimization algorithms increases but most of them were verified only on synthetic tests). Also, it should be noted that all mentioned problems lead to so‑called reproducibility crisis. The main idea of this work is to suggest an Open-Source Optimization Library Extremum (OSOL Extremum) with wide API features.
</p>

# Contents
* [Project structure](#project-structure)
	* [Cores](#cores)
	* [PyTools](#pytools)
	* [Algorithms](#algorithms)
	* [Apps](#apps)
* [Usage info](#usage-info)
	* [Out-of-box usage](#out-of-box-usage)
	* [Task preparation](#task-preparation)
		* [Unconstrained optimization](#unconstrained-optimization)
		* [Openloop control](#openloop-control)
	* [Algorithm development](#algorithm-develoment)
		* [JVM Core](#jvm-core)
			* [Scala](#scala)
			* [Java](#java)
		* [.Net Core](#net-core)
			* [C#](#c)
			* [F#](#f)
* [Implemented algorithms](#implemented-algorithms)
	* [Table of algorithms](#table-of-algorithms)
	* [Random Search](#random-search)
	* [Interval Explosion Search](#interval-explosion-search)
	* [Differential Evolution](#differential-evolution)
* [Articles about OSOL.Extremum projects](#articles-about-osolextremum-projects)

# Project structure

OSOL.Extremum consists of four main parts:
* Cores
* PyTools
* Algorithms
* Apps

Overall structure and inner connections are shown below:

![Project Structure](Description/OSOL.Extremum.png?raw=true "Project Structure")

Besides, there are several blocks which mostly play support role:
* Configs - contains examples of algorithms' configuration files,
* Tasks - contains examples of tasks' configuration files.

## Cores

Current module contains implementation of algorithmic cores (JVM, written in scala, and .Net, written in C#, versions). These cores provide basic functionality for algorithm development and further usage. 

Version history:

*Ver. № 0.0.7.\**
- [ ] automated testing on general benchmarks functions,
- [ ] A/B testing of different algorithms,
- [ ] "continue" mode.

**Ver. № 0.0.6.\***
- [x] state logging feature.

~~Ver. № 0.0.5.\*~~
- [x] algorithms are described as a transition graph between nodes, which represent steps of optimization procedure,
- [x] basic vector arithmetic,
- [x] unified form of GoRN - generator of random numbers,
- [x] automated testing of algorithm using dummy functions,
- [x] support of interval vectors (boxes) for interval optimization algorithms,
- [x] dummy examples how to create an algorithm using cores.


## PyTools

Version history:

*Ver. № 0.5.\**
- [ ] supported tasks: optimal stochastic control.

*Ver. № 0.4.\**
- [ ] visualization of algorithms,
- [ ] incremental optimization,
- [ ] chain optimization.

*Ver. № 0.3.\**
- [ ] supported tasks: optimal stochastic control.

*Ver. № 0.2.\**
- [ ] supported tasks: constrained optimization, linear regression task.

**Ver. № 0.1.\***
- [x] supported tasks: unconstrained optimization, optimal openloop control,
- [x] implementation of interval arithmetics,
- [x] modelling of dynamic systems using Euler and Runge-Kutta discretization processes,
- [x] supported types of controllers: piecewise-constant, piecewise-linear, explicit.

## Algorithms

Current module contains code for optimization algorithms. Better description is provided in the following section: [Implemented algorithms](#implemented-algorithms).

## Apps

Current module contains implementation of various apps built using this project. 

List of apps:
* Runner (JVM) - used to run [implemented algorithms](#implemented-algorithms) for JVM Core,
* Runner (.Net) - used to run [implemented algorithms](#implemented-algorithms) for .Net Core.

# Usage info

** Under construction **

## Out-of-box usage

## Task preparation

### Unconstrained optimization

### Openloop control

## Algorithm development

### JVM CORE

#### Scala

#### Java

### .Net Core

#### C\#

#### F\#

# Implemented algorithms
<p align="justify">
Current section will provide information about algorithms that are currently implemented in OSOL Extremum.
</p>

## Table of algorithms

| Name | Description | Scala | Java |  C#  |  F#  | Supports seed value |
| ---- | ----------- | :---: | :--: | :--: | :--: | :-----------------: |
| Random Search (RS) | [Wiki](https://en.wikipedia.org/wiki/Random_search) | + | + | + | + | Scala |
| Interval Explosion Search (IES) | [Trudy MAI](http://trudymai.ru/upload/iblock/b78/b783155b46dd299b9cecc91637821acc.pdf), [South Ural State University Bulletin](http://mmp.susu.ru/pdf/v9n3st5.pdf) | + | - | - | - | Scala |
| Differential Evolution (DE) | no link | - | - | + | - | No |

## Random Search

RS in one of the simplest metaheuristic optimization algorithm. Its idea is to sample points near the current one (which is treated as an approximate solution). When point with better value of target function is found algorithms starts using it as the approximate solution and the whole procedure repeats until termination criterion is met.

### Config example

```json
{
	"language": "Language Name",
	"algorithm": "RS",
	"radius": 1.0,
	"maxTime": 60.0	
}
```

Notes:
* available languages are: "Scala", "Java", "CSharp", "FSharp",
* "RS" can be substituted with the full name "RandomSearch".

### Benchmark Results

**Under Construction**

## Interval Explosion Search

IES is built using the following heuristics:
* boxes with bad value of fitness function can move for longer distances,
* boxes with good value of fitness functions should not move for long distances.

Thus, IES tries to balance between global search due to the existence of the opportunity to make relatively huge gaps coupled with an ability to make local search.

### Config example

```json
{
	"language": "Language Name",
	"algorithm": "IES",
	"maxBombs": 20,
	"rMax": 
	[
		{
			"name": "x",
			"value": 1.0
		},
		{
			"name": "y",
			"value": 1.0
		},
		{
			"name": "z",
			"value": 1.0
		}
	],
	"maxTime": 60.0	
}
```

Notes:
* available language is: "Scala",
* "IES" can be substituted with the full name "IntervalExplosionSearch".

### Benchmark Results

**Under Construction**

## Differential Evolution

According to [Jason Brownlee](http://www.cleveralgorithms.com):
>The Differential Evolution algorithm involves maintaining a population of candidate solutions subjected to iterations of recombination, evaluation, and selection. The recombination approach involves the creation of new candidate solution components based on the weighted difference between two randomly selected population members added to a third population member. This perturbs population members relative to the spread of the broader population. In conjunction with selection, the perturbation effect self-organizes the sampling of the problem space, bounding it to known areas of interest.

### Config example

```json
{
	"language": "Language Name",
	"algorithm": "DE",
	"populationSize": 10,
	"weightingFactor": 0.5,
	"crossoverRate": 0.75,
	"maxTime": 60.0	
}
```

Notes:
* available language is: "CSharp",
* "DE" can be substituted with the full name "DifferentialEvolution".

### Benchmark Results

**Under Construction**

# Articles about OSOL.Extremum projects

**Under Construction**

