package kaimere.real.optimization.basic

import kaimere.real.objects.{RealVector, Function}
import OptimizationAlgorithm.Area
import OptimizationAlgorithm.MergeStrategy.MergeStrategy

abstract class OptimizationAlgorithm {

  protected var f: Function = null
  protected var area: Area = null
  protected var currentState: State = null

  def initialize(f: Function, area: Area, state: Vector[Map[String, Double]], mergeStrategy: MergeStrategy): Unit = {
    this.f = f
    this.area = area
    this.currentState = merge(state, mergeStrategy)
  }

  def merge(state: Vector[Map[String, Double]], mergeStrategy: MergeStrategy): State

  def iterate(): Unit

  final def work(instruction: Instruction): RealVector = {
    instruction.reset()
    while(instruction.continue())
      iterate()
    currentState.getBestBy(f)
  }

}

object OptimizationAlgorithm {

  type Area = Map[String, (Double, Double)]

  object MergeStrategy extends Enumeration {
    type MergeStrategy = Value
    val force = Value
  }

}
