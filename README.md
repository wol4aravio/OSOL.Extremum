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

Adaptive Random Search (ARS) [[1](#references)] enriches classical Random Search (RS) [[1](#references)] with the
procedure of search radius update.

### Config Example

### Benchmark Results

## Interval Explosion Search

Current algorithm is based on several heuristics [[8](#references)]:
* solution candidates with better function value will slightly change position, on the
opposite – candidates with worse function value have a potential to greatly change
position,
* during explosion phase (when new solutions are generated) search is performed by
all possible direction along one axis.

### Config Example

### Benchmark Results

## Luus-Jaakola Optimization

Procedure of Modified Luus-Jaakola Optimization (LJO) is very similar to classic RS 
with the exception that search area is reduced and then restored during execution [[3, 4](#references)] 

### Config Example

### Benchmark Results

## Modified Hybrid Memetic Algorithm

Term ”Memetic Algorithm” is widely used to denote an interaction between evolutionary
and other approach basing on the definition of population coupled with local improvement 
procedure. Firstly it was proposed in [[5 - 7](#references)] and had a form of hybrid of genetic 
algorithm with individual learning process to make a solution more accurate.

The proposed algorithm uses cultural evolution component which is realized as an internal
optimization sub-task. During the process of cultural evolution information of population
members is used to construct new solutions.

### Config Example

### Benchmark Results

## Modified Hybrid Random Search

### Config Example

### Benchmark Results

## Random Search

[Random search](https://en.wikipedia.org/wiki/Random_search) is a family of numerical optimization 
methods that do not require the gradient of the problem to be optimized, and RS can hence be used on 
functions that are not continuous or differentiable. Such optimization methods are also known as 
direct-search, derivative-free, or black-box methods.

### Config Example

### Benchmark Results

## Random Search with Statistical Anti Gradient

Random Search with Statistical Anti Gradient (RSwSAG) modifies current solution by anti gradient that is calculated over a set of samples [[2](#references)].

### Config Example

### Benchmark Results

## Simulated Annealing

[Simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing) (SA) is a probabilistic technique 
for approximating the global optimum of a given function. Specifically, it is a metaheuristic to approximate 
global optimization in a large search space. It is often used when the search space is discrete (e.g., all tours 
that visit a given set of cities). For problems where finding an approximate global optimum is more important than 
finding a precise local optimum in a fixed amount of time, simulated annealing may be preferable to alternatives such 
as gradient descent.

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

# References

[1] Gendreau M., and Potvin J.-S. 2010. Handbook of Metaheuristics. New York: Springer

[2] Theodoridis S. 2015. Machine Learning. A Bayesian and Optimization Perspective. NY: Academic Press.

[3] Luus R. 2000. Iterative Dynamic Programming. Monographs and Surveys in Pure and Applied Mathematics. London: Chapman & Hall, CRC Press.

[4] Luus R., Jaakola T.H.I. 1973. ”Optimization by direct search and systematic reduction of the size of search region”. American Institute of Chemical Engineers Journal 19(4): 760 – 766.

[5] Brownlee J. 2011. Clever Algorithms: Nature-Inspired Programming Recipes. North Carolina, Morrisville: LuLu.

[6] Moscato P., Cotta C. 2010. ”A Modern Introduction to Memetic Algorithms”. In Handbook of Metaheuristics edited by Michel Gendreau and Jean-Yves Potvin, 141 – 184. London: Springer.

[7] Panteleev A.V., Pis’mennaya V.A. 2018. ”Application of a Memetic Algorithm for the Optimal Control of Bunches of Trajectories of Nonlinear Deterministic Systems with Incomplete Feedback”. Journal of Computer and Systems Sciences International 57(1): 25 – 36.

[8] Panteleev A.V., Panovskiy V.N., Korotkova T.I. 2016. ”Interval explosion search algorithm and its application to hypersonic aircraft modelling and motion optimization problems”. Bulletin of the South Ural State University, Series: Mathematical Modelling, Programming and Computer Software 9: 55 – 67.

# Articles about OSOL.Extremum Project
