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
* [Project Structure](#project-structure)
	* [Numerical Objects](#numerical-objects)
		* [Interval](#interval)
		* [Vector](#vector)
	* [Cybernatics](#cybernatics)
		* [Dynamic System](#dynamic-system)
		* [Controllers](#controllers)
	* [Optimization](#optimization)
		* [Algorithms](#algorithms)
		* [Terminators](#terminators)
		* [Tasks](#tasks)
		* [Verifier](#verifier)
	* [Tools](#algorithms)
		* [Encoders](#encoders)
		* [Optimization Tools](#optimization-tools)
		* [etc](#etc)
	* [Applications](#applications)
		* [Benchmark](#benchmark)
		* [Optimize](#optimize)
		* [Simulate](#simulate)
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
* [Articles about OSOL.Extremum Projects](#articles-about-osolextremum-projects)

# Project Structure

##  Numerical Objects

### Interval

### Vector

## Cybernatics

### Dynamic System

### Controllers

## Optimization

### Algorithms

### Terminators

### Tasks

### Verifier

## Tools

### Encoders

### Optimization Tools

### etc

## Applications

### Benchmark

### Optimize

### Simulate

# Implemented Algorithms

## Adaptive Random Search

## Interval Explosion Search

## Luus-Jaakola Optimization

## Modified Hybrid Memetic Algorithm

## Modified Hybrid Random Search

## Random Search

## Random Search with Statistical Anti Gradient

## Simulated Annealing

# Current State

- [x] ~~supported tasks: unconstrained optimization~~
- [x] ~~supported tasks: optimal openloop control~~
- [ ] supported tasks: constrained optimization
- [ ] supported tasks: optimal feedback control
- [ ] supported tasks: optimal stochastic control

- [x] ~~features: implementation of interval arithmetics~~
- [x] ~~features: state logging~~
- [ ] features: custom callbacks

- [x] ~~modelling of dynamic systems using Euler discretization processes~~
- [x] ~~modelling of dynamic systems using Runge-Kutta (IV order) discretization processes~~

- [x] ~~supported types of controllers: piecewise-constant~~
- [x] ~~supported types of controllers: piecewise-linear~~
- [x] ~~supported types of controllers: explicit~~
- [ ] supported types of controllers: via decomposition by basis

- [x] ~~benchmarking: <= 10 test functions (2D)~~
- [ ] benchmarking: <= 25 test functions (2D)
- [ ] benchmarking: <= 50 test functions (2D)

- [x] ~~implemented algorithms: Adaptive Random Search~~
- [x] ~~implemented algorithms: Interval Explosion Search~~
- [x] ~~implemented algorithms: Luus-Jaakola Optimization~~
- [x] ~~implemented algorithms: Modified Hybrid Memetic Algorithm~~
- [x] ~~implemented algorithms: Modified Hybrid Random Search~~
- [x] ~~implemented algorithms: Random Search~~
- [x] ~~implemented algorithms: Random Search with Statistical Anti Gradient~~
- [x] ~~implemented algorithms: Simulated Annealing~~
- [ ] implemented algorithms: Interval Genetic Algorithm with Ternary Coding
- [ ] implemented algorithms: Metaheuristic Interval Inversed Search
- [ ] implemented algorithms: Differential Evolution

# Articles about OSOL.Extremum Projects
