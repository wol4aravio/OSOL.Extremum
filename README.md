[![Build Status](https://travis-ci.org/wol4aravio/OSOL.Extremum.svg?branch=master)](https://travis-ci.org/wol4aravio/OSOL.Extremum.svg?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6d29733e0b2d4faea9b99306ecff0f91)](https://www.codacy.com/app/wol4aravio/OSOL.Extremum?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wol4aravio/OSOL.Extremum&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/6d29733e0b2d4faea9b99306ecff0f91)](https://www.codacy.com/app/wol4aravio/OSOL.Extremum?utm_source=github.com&utm_medium=referral&utm_content=wol4aravio/OSOL.Extremum&utm_campaign=Badge_Coverage)

<p align="center">
<b> Open-Source Optimization Library - Extremum </b>
</p>

<p align="justify">
Optimization theory is a widely-used field of mathematics that can be applied to different tasks: pure engineering problems (e.g., obtaining optimal wing shape), control synthesis tasks (e.g., determination of optimal guidance of aircraft), and even machine learning (e.g., training procedures of neural networks). Currently mostly all applied software systems support optimization procedures in a very limited form. This fact leads to several problems: black-box effect (i.e., there is no opportunity to explore source code, modify it, or simply verify), no code reuse (i.e., implemented procedures are accessible only within software that includes it), limitation of modern optimization algorithm application (i.e., number of optimization algorithms increases but most of them were verified only on synthetic tests). Also, it should be noted that all mentioned problems lead to so‑called reproducibility crisis. The main idea of this work is to suggest an Open-Source Optimization Library Extremum (OSOL Extremum) with wide API features.
</p>

# Contents
* [Project Structure](#project-structure)
* [Implemented algorithms](#implemented-algorithms)
	* [Adaptive Random Search](#adaptive-random-search)
	* [Interval Explosion Search](#interval-explosion-search)
	* [Luus-Jaakola Optimization](#luus-jaakola-optimization)
	* [Modified Hybrid Memetic Algorithm](#modified-hybrid-memetic-algorithm)
	* [Modified Hybrid Random Search](#modified-hybrid-random-search)
	* [Random Search](#random-search)
	* [Random Search with Statistical Anti Gradient](#random-search-with-statistical-anti-gradient)
	* [Simulated Annealing](#simulated-annealing)
* [Current State](#current-state)
* [References](#references)
* [Articles about OSOL.Extremum Project](#articles-about-osolextremum-projects)

# Project Structure

**Numerical Objects** module contains [interval arithmetics](Examples/NumericalObjects.Intervals.ipynb) and [vector](Examples/NumericalObjects.Vectors.ipynb) operations.

**Cybernetics** module implements dynamic systems with different types of controllers.

**Optimization** module implements all required levels of abstraction of optimization algorithms and contains realization of various metaheuristic optimization algithms and tasks that can be solved via them.

**Tools** module contains various procedures and classes to connect modules together and provide convenient input/output methods (including JSON serialization).

**Applications** module contains scripts that are targeted on solution of a real problem, e.g. to apply optimization algorithm to the given task, to simulate dynamic system behavior using provided controls, evaluate algorithm's efficiency on benchmark set.

# Implemented Algorithms

## Adaptive Random Search

[Adaptive Random Search](Gendreau) (ARS) enriches classical [Random Search](Gendreau) (RS) with the
procedure of search radius update.

### Config Example

### Benchmark Results

## Interval Explosion Search

### Config Example

### Benchmark Results

## Luus-Jaakola Optimization

### Config Example

### Benchmark Results

## Modified Hybrid Memetic Algorithm

### Config Example

### Benchmark Results

## Modified Hybrid Random Search

### Config Example

### Benchmark Results

## Random Search

### Config Example

### Benchmark Results

## Random Search with Statistical Anti Gradient

### Config Example

### Benchmark Results

## Simulated Annealing

### Config Example

### Benchmark Results

# Current State

- [x] ~~__supported tasks__: unconstrained optimization~~
- [x] ~~__supported tasks__: optimal openloop control~~
- [ ] __supported tasks__: constrained optimization
- [ ] __supported tasks__: optimal feedback control
- [ ] __supported tasks__: optimal stochastic control

<br/>

- [x] ~~__features__: implementation of interval arithmetics~~
- [x] ~~__features__: state logging~~
- [ ] __features__: custom callbacks
- [ ] __features__: termination via max iterations

<br/>

- [x] ~~__modelling of dynamic systems__: Euler discretization processes~~
- [x] ~~__modelling of dynamic systems__: Runge-Kutta (IV order) discretization processes~~

<br/>

- [x] ~~__supported types of controllers__: piecewise-constant~~
- [x] ~~__supported types of controllers__: piecewise-linear~~
- [x] ~~__supported types of controllers__: explicit~~
- [ ] __supported types of controllers__: via decomposition by basis

<br/>

- [x] ~~__application__: solution of optimization task~~
- [x] ~~__application__: benchmarking of an algorithm configuration~~
- [x] ~~__application__: simulation of a control~~
- [ ] __application__: algorithms comparison
- [ ] __application__: algorithm visualization

<br/>

- [x] ~~__benchmarking__: <= 10 test functions (2D)~~
- [ ] __benchmarking__: <= 25 test functions (2D)
- [ ] __benchmarking__: <= 50 test functions (2D)

<br/>

- [x] ~~__implemented algorithms__: Adaptive Random Search~~
- [x] ~~__implemented algorithms__: Interval Explosion Search~~
- [x] ~~__implemented algorithms__: Luus-Jaakola Optimization~~
- [x] ~~__implemented algorithms__: Modified Hybrid Memetic Algorithm~~
- [x] ~~__implemented algorithms__: Modified Hybrid Random Search~~
- [x] ~~__implemented algorithms__: Random Search~~
- [x] ~~__implemented algorithms__: Random Search with Statistical Anti Gradient~~
- [x] ~~__implemented algorithms__: Simulated Annealing~~
- [ ] __implemented algorithms__: Interval Genetic Algorithm with Ternary Coding
- [ ] __implemented algorithms__: Metaheuristic Interval Inversed Search
- [ ] __implemented algorithms__: Differential Evolution

# Articles about OSOL.Extremum Project

[Gendreau]: Gendreau M., and Potvin J.-S. 2010. Handbook of Metaheuristics. New York: Springer

