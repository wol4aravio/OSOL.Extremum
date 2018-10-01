[![Build Status](https://travis-ci.org/wol4aravio/OSOL.Extremum.svg?branch=master)](https://travis-ci.org/wol4aravio/OSOL.Extremum.svg?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6d29733e0b2d4faea9b99306ecff0f91)](https://www.codacy.com/app/wol4aravio/OSOL.Extremum?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wol4aravio/OSOL.Extremum&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/6d29733e0b2d4faea9b99306ecff0f91)](https://www.codacy.com/app/wol4aravio/OSOL.Extremum?utm_source=github.com&utm_medium=referral&utm_content=wol4aravio/OSOL.Extremum&utm_campaign=Badge_Coverage)
[![PyPI version](https://badge.fury.io/py/osol.extremum.svg)](https://badge.fury.io/py/osol.extremum)
[![Docs](https://readthedocs.org/projects/osolextremum/badge/?version=latest)](https://readthedocs.org/projects/osolextremum/badge/?version=latest)

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
* [Example of algorithm application](Examples/Optimization.Demo.ipynb),
* [Example of algorithm benchmarking](Examples/Optimization.Benchmarking.ipynb).

**Tools** module contains various procedures and classes to connect modules together and provide convenient input/output methods (including JSON serialization).

**Applications** module contains scripts that are targeted on solution of a real problem, e.g. to apply optimization algorithm to the given task, to simulate dynamic system behavior using provided controls, evaluate algorithm's efficiency on benchmark set.

# Implemented Algorithms

## Adaptive Random Search

Adaptive Random Search (ARS) [[1](#references)] enriches classical Random Search (RS) [[1](#references)] with the
procedure of search radius update.

### Config Example

```json
{
  "AdaptiveRandomSearch": {
    "init_radius": 1.0,
    "factor_small": 1.1,
    "factor_huge": 1.5,
    "frequency": 5,
    "max_no_change": 5
  }
}
```

### Benchmark Results

| Function name | Optimal value | Min value | Mean value | Max value | Standard deviation |
| ------------- | :-----------: | :-------: | :--------: | :-------: | :----------------: |
| Ackley | -22.71828 | -22.71828 | -4.05817 | -2.77192 | 2.88728 |
| Beale | 0.00000 | 0.00000 | 1.40197 | 8.98086 | 2.66703 |
| CosineMixture | -0.20000 | -0.20000 | -0.20000 | -0.20000 | 0.00000 |
| DropWave | -1.00000 | -1.00000 | -0.93238 | -0.15277 | 0.11691 |
| Exponential | -1.00000 | -1.00000 | -1.00000 | -1.00000 | 0.00000 |
| FreudensteinRoth | 0.00000 | 0.00000 | 29.37954 | 49.79582 | 24.49124 |
| GoldsteinPrice | 3.00000 | 3.00000 | 17.04000 | 84.00000 | 30.42266 |
| HimmelBlau | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| Leon | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| Rastrigin | -400.00000 | -400.00000 | -228.66881 | 236.76975 | 162.85383 |

## Interval Explosion Search

Current algorithm is based on several heuristics [[8](#references)]:
* solution candidates with better function value will slightly change position, on the
opposite – candidates with worse function value have a potential to greatly change
position,
* during explosion phase (when new solutions are generated) search is performed by
all possible direction along one axis.

### Config Example

```json
{
  "IntervalExplosionSearch": {
    "max_bombs": 10,
    "max_radius_ratio": 0.1
  }
}
```

### Benchmark Results

| Function name | Optimal value | Min value | Mean value | Max value | Standard deviation |
| ------------- | :-----------: | :-------: | :--------: | :-------: | :----------------: |
| Ackley | -22.71828 | -22.71813 | -22.71690 | -22.71521 | 0.00067 |
| Beale | 0.00000 | 0.00000 | 0.00001 | 0.00005 | 0.00001 |
| CosineMixture | -0.20000 | -0.20000 | -0.20000 | -0.20000 | 0.00000 |
| DropWave | -1.00000 | -1.00000 | -0.99999 | -0.99991 | 0.00001 |
| Exponential | -1.00000 | -1.00000 | -1.00000 | -1.00000 | 0.00000 |
| FreudensteinRoth | 0.00000 | 0.00000 | 13.44497 | 49.79582 | 22.10727 |
| GoldsteinPrice | 3.00000 | 3.00000 | 3.00003 | 3.00018 | 0.00003 |
| HimmelBlau | 0.00000 | 0.00000 | 0.00002 | 0.00010 | 0.00002 |
| Leon | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| Rastrigin | -400.00000 | -399.99998 | -399.99811 | -399.98947 | 0.00232 |

## Luus-Jaakola Optimization

Procedure of Modified Luus-Jaakola Optimization (LJO) is very similar to classic RS 
with the exception that search area is reduced and then restored during execution [[3, 4](#references)] 

### Config Example

```json
{
  "LuusJaakolaOptimization": {
    "init_radius": 1.0,
    "number_of_samples": 5,
    "reduction_coefficient": 0.95,
    "recover_coefficient": 0.97,
    "iteration_per_run": 5
  }
}
```

### Benchmark Results

| Function name | Optimal value | Min value | Mean value | Max value | Standard deviation |
| ------------- | :-----------: | :-------: | :--------: | :-------: | :----------------: |
| Ackley | -22.71828 | -22.71828 | -4.00004 | -2.76720 | 2.48257 |
| Beale | 0.00000 | 0.00000 | 1.59728 | 9.28137 | 2.76872 |
| CosineMixture | -0.20000 | -0.20000 | -0.20000 | -0.20000 | 0.00000 |
| DropWave | -1.00000 | -1.00000 | -0.96878 | -0.61950 | 0.04713 |
| Exponential | -1.00000 | -1.00000 | -1.00000 | -1.00000 | 0.00000 |
| FreudensteinRoth | 0.00000 | 0.00000 | 26.39179 | 49.79582 | 24.85306 |
| GoldsteinPrice | 3.00000 | 3.00000 | 18.39000 | 84.00000 | 31.77637 |
| HimmelBlau | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| Leon | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| Rastrigin | -400.00000 | -380.10082 | -108.08053 | 415.85933 | 194.56416 |

## Modified Hybrid Memetic Algorithm

Term ”Memetic Algorithm” is widely used to denote an interaction between evolutionary
and other approach basing on the definition of population coupled with local improvement 
procedure. Firstly it was proposed in [[5 - 7](#references)] and had a form of hybrid of genetic 
algorithm with individual learning process to make a solution more accurate.

The proposed algorithm uses cultural evolution component which is realized as an internal
optimization sub-task. During the process of cultural evolution information of population
members is used to construct new solutions.

### Config Example

```json
{
  "ModifiedHybridMemeticAlgorithm": {
    "population_size": 10,
    "distance_bias": 0.1,
    "pool_size": 5,
    "pool_purge_size": 5,
    "combination_algorithm": {
      "RandomSearch": {
        "radius": 0.1
      }
    },
    "combination_terminator": {
      "MaxTimeTerminator": {
        "max_time": "s:0.1"
      }
    },
    "path_relinking_parameter": 5,
    "local_improvement_parameter": 5,
    "delta_path_relinking": 5,
    "delta_local_improvement": 0.01
  }
}
```

### Benchmark Results

| Function name | Optimal value | Min value | Mean value | Max value | Standard deviation |
| ------------- | :-----------: | :-------: | :--------: | :-------: | :----------------: |
| Ackley | -22.71828 | -22.71828 | -22.71777 | -22.71388 | 0.00090 |
| Beale | 0.00000 | 0.00000 | 0.00000 | 0.00003 | 0.00000 |
| CosineMixture | -0.20000 | -0.20000 | -0.20000 | -0.20000 | 0.00000 |
| DropWave | -1.00000 | -1.00000 | -1.00000 | -0.99990 | 0.00001 |
| Exponential | -1.00000 | -1.00000 | -1.00000 | -1.00000 | 0.00000 |
| FreudensteinRoth | 0.00000 | 0.00000 | 0.00002 | 0.00145 | 0.00014 |
| GoldsteinPrice | 3.00000 | 3.00000 | 3.00001 | 3.00016 | 0.00003 |
| HimmelBlau | 0.00000 | 0.00000 | 0.00001 | 0.00006 | 0.00001 |
| Leon | 0.00000 | 0.00000 | 0.00023 | 0.00615 | 0.00086 |
| Rastrigin | -400.00000 | -400.00000 | -399.99998 | -399.99933 | 0.00007 |

## Modified Hybrid Random Search

Modified Hybrid Random Search (MHRS) consequently uses several simpler optimization procedures.

### Config Example

```json
{
  "ModifiedHybridRandomSearch": {
    "algorithms": [
      {
        "AdaptiveRandomSearch": {
          "init_radius": 1.0,
          "factor_small": 1.1,
          "factor_huge": 1.5,
          "frequency": 5,
          "max_no_change": 5
        }
      },
      {
        "RandomSearchWithStatisticalAntiGradient": {
          "radius": 1.0,
          "number_of_samples": 5
        }
      },
      {
        "LuusJaakolaOptimization": {
          "init_radius": 1.0,
          "number_of_samples": 5,
          "reduction_coefficient": 0.95,
          "recover_coefficient": 0.97,
          "iteration_per_run": 5
        }
      }
    ],
    "terminators": [
      {
        "MaxTimeTerminator": {
          "max_time": "s:5"
        }
      },
      {
        "MaxTimeTerminator": {
          "max_time": "s:5"
        }
      },
      {
        "MaxTimeTerminator": {
          "max_time": "s:5"
        }
      }
    ]
  }
}
```

### Benchmark Results

| Function name | Optimal value | Min value | Mean value | Max value | Standard deviation |
| ------------- | :-----------: | :-------: | :--------: | :-------: | :----------------: |
| Ackley | -22.71828 | -22.71828 | -5.98708 | -2.77883 | 6.54783 |
| Beale | 0.00000 | 0.00000 | 0.86048 | 9.01775 | 2.19928 |
| CosineMixture | -0.20000 | -0.20000 | -0.20000 | -0.20000 | 0.00000 |
| DropWave | -1.00000 | -1.00000 | -1.00000 | -1.00000 | 0.00000 |
| Exponential | -1.00000 | -1.00000 | -1.00000 | -1.00000 | 0.00000 |
| FreudensteinRoth | 0.00000 | 0.00000 | 25.89383 | 49.79582 | 24.87799 |
| GoldsteinPrice | 3.00000 | 3.00000 | 16.77000 | 84.00000 | 30.42626 |
| HimmelBlau | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| Leon | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| Rastrigin | -400.00000 | -400.00000 | -312.64288 | 177.07108 | 128.86537 |

## Random Search

[Random search](https://en.wikipedia.org/wiki/Random_search) is a family of numerical optimization 
methods that do not require the gradient of the problem to be optimized, and RS can hence be used on 
functions that are not continuous or differentiable. Such optimization methods are also known as 
direct-search, derivative-free, or black-box methods.

### Config Example
```json
{
  "RandomSearch": {
    "radius": 1.0
  }
}
```

### Benchmark Results

| Function name | Optimal value | Min value | Mean value | Max value | Standard deviation |
| ------------- | :-----------: | :-------: | :--------: | :-------: | :----------------: |
| Ackley | -22.71828 | -22.71826 | -22.12810 | -2.80858 | 3.35485 |
| Beale | 0.00000 | 0.00000 | 1.30965 | 8.49208 | 2.76080 |
| CosineMixture | -0.20000 | -0.20000 | -0.20000 | -0.20000 | 0.00000 |
| DropWave | -1.00000 | -1.00000 | -1.00000 | -0.99999 | 0.00000 |
| Exponential | -1.00000 | -1.00000 | -1.00000 | -1.00000 | 0.00000 |
| FreudensteinRoth | 0.00000 | 0.00000 | 31.86933 | 49.79582 | 23.90199 |
| GoldsteinPrice | 3.00000 | 3.00000 | 20.01001 | 84.00014 | 32.99198 |
| HimmelBlau | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| Leon | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| Rastrigin | -400.00000 | -400.00000 | -399.99999 | -399.99995 | 0.00001 |

## Random Search with Statistical Anti Gradient

Random Search with Statistical Anti Gradient (RSwSAG) modifies current solution by anti gradient that is calculated over a set of samples [[2](#references)].

### Config Example

```json
{
  "RandomSearchWithStatisticalAntiGradient": {
    "radius": 1.0,
    "number_of_samples": 5
  }
}
```

### Benchmark Results

| Function name | Optimal value | Min value | Mean value | Max value | Standard deviation |
| ------------- | :-----------: | :-------: | :--------: | :-------: | :----------------: |
| Ackley | -22.71828 | -22.71797 | -6.11105 | -2.05663 | 6.85998 |
| Beale | 0.00000 | 0.00012 | 0.63264 | 9.42809 | 1.15283 |
| CosineMixture | -0.20000 | -0.20000 | -0.20000 | -0.19999 | 0.00000 |
| DropWave | -1.00000 | -1.00000 | -1.00000 | -0.99998 | 0.00000 |
| Exponential | -1.00000 | -1.00000 | -1.00000 | -1.00000 | 0.00000 |
| FreudensteinRoth | 0.00000 | 0.96336 | 90.84234 | 213.05327 | 45.22504 |
| GoldsteinPrice | 3.00000 | 3.00193 | 5.88163 | 12.21118 | 2.20215 |
| HimmelBlau | 0.00000 | 0.00162 | 0.61417 | 2.46690 | 0.47214 |
| Leon | 0.00000 | 0.00005 | 0.10794 | 0.26133 | 0.06735 |
| Rastrigin | -400.00000 | -400.00000 | -284.47774 | 419.41124 | 177.54471 |

## Simulated Annealing

[Simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing) (SA) is a probabilistic technique 
for approximating the global optimum of a given function. Specifically, it is a metaheuristic to approximate 
global optimization in a large search space. It is often used when the search space is discrete (e.g., all tours 
that visit a given set of cities). For problems where finding an approximate global optimum is more important than 
finding a precise local optimum in a fixed amount of time, simulated annealing may be preferable to alternatives such 
as gradient descent.

### Config Example

```json
{
  "SimulatedAnnealing": {
    "init_temperature": 25.0,
    "C": 0.85,
    "beta": 0.99
  }
}
```

### Benchmark Results

| Function name | Optimal value | Min value | Mean value | Max value | Standard deviation |
| ------------- | :-----------: | :-------: | :--------: | :-------: | :----------------: |
| Ackley | -22.71828 | -22.71828 | -15.87059 | -2.76310 | 9.22266 |
| Beale | 0.00000 | 0.00000 | 0.23205 | 0.82458 | 0.31806 |
| CosineMixture | -0.20000 | -0.20000 | -0.20000 | -0.20000 | 0.00000 |
| DropWave | -1.00000 | -1.00000 | -0.70044 | -0.07951 | 0.32082 |
| Exponential | -1.00000 | -1.00000 | -1.00000 | -1.00000 | 0.00000 |
| FreudensteinRoth | 0.00000 | 0.00000 | 6.97142 | 49.79582 | 17.27851 |
| GoldsteinPrice | 3.00000 | 3.00000 | 4.62000 | 84.00000 | 11.34000 |
| HimmelBlau | 0.00000 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| Leon | 0.00000 | 0.00000 | 0.00002 | 0.00046 | 0.00007 |
| Rastrigin | -400.00000 | -400.00000 | -387.86150 | -360.20164 | 11.21968 |

# Current State

## Version 0.1.*

* **supported tasks**: unconstrained optimization, optimal openloop control,
* **algorithms**: Adaptive Random Search, Interval Explosion Search, Luus-Jaakola Optimization,
Modified Hybrid Memetic Algorithm, Modified Hybrid Random Search, Random Search,
Random Search with Statistical Anti Gradient, Simulated Annealing,
* **cybernetics**: 
    * **discretization**: Euler, Runge-Kutta (IV order),
    * **controllers**: piecewise-constant, piecewise-linear, explicit,
* **applications**: solution of optimization task, benchmarking of an algorithm configuration,
simulation of a control,
* **miscellaneous**: implementation of interval arithmetics, state logging.

## Planned

* **supported tasks**: constrained optimization, optimal feedback control, optimal stochastic control,
* **algorithms**: Interval Genetic Algorithm with Ternary Coding, Metaheuristic Interval Inversed Search,
Differential Evolution,
* **cybernetics**: controller via decomposition by basis,
* **applications**: algorithms comparison, algorithm visualization,
* **miscellaneous**: custom callbacks, termination via max iterations, termination via max function evaluation, 
PyTorch integration.

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
