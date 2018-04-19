namespace OSOL.Extremum.Algorithms.FSharp

open System
open System.Collections.Generic
open System.Linq
open System.Runtime.CompilerServices
open OSOL.Extremum.Cores.DotNet.Optimization
open OSOL.Extremum.Cores.DotNet.Vectors
open OSOL.Extremum.Cores.DotNet.Optimization.Nodes
open OSOL.Extremum.Cores.DotNet.Random
open OSOL.Extremum.Cores.DotNet.Random.Distributions

[<AbstractClass; Sealed>]
type RandomSearch =
    static member CurrentPointName = "currentPoint"
    static member CurrentPointEfficiencyName = "currentPointEfficiency"
    static member RadiusParameterName = "r"
    static member GoRN = new GoRN()
    
    static member GenerateRandomInSphere (currentPoint: RealVector) (radius: double) (area: Dictionary<string, double * double>) =
        let normallyDistributed = area.ToDictionary ((fun kvp -> kvp.Key), (fun kvp -> (0.0, 1.0)))
                                  |> RandomSearch.GoRN.GetNormalVector
                                  |> RealVector.op_Implicit
                                  
        let r = normallyDistributed.Elements.Values
                |> Seq.map (fun x -> x * x)
                |> Seq.sum
                
        new RealVector(currentPoint + new RealVector(normallyDistributed * (RandomSearch.GoRN.GetContinuousUniform(-1.0, 1.0) / r)))
        
    type GenerateInitialPointNode = 
        inherit GeneralNode<RealVector, double, RealVector> 
        
        new (nodeId: int) as this = { } then this.NodeId <- nodeId
        
        override this.Initialize(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) = 
            let initialPoint: RealVector = RandomSearch.GoRN.GetContinuousUniformVector(area) |> RealVector.op_Implicit
            state.SetParameter(RandomSearch.CurrentPointName, initialPoint)
            state.SetParameter(RandomSearch.CurrentPointEfficiencyName, initialPoint.GetPerformance(f))
            ()
        
        override this.Process(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) = ()
    
    type SampleNewPointNode_FixedStep = 
        inherit GeneralNode<RealVector, double, RealVector>
        
        new (nodeId: int) as this = { } then this.NodeId <- nodeId
        
        override this.Initialize(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) = ()

        override this.Process(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) =
            let currentPoint = state.GetParameter<RealVector>(RandomSearch.CurrentPointName)
            let currentPointEfficiency = state.GetParameter<Double>(RandomSearch.CurrentPointEfficiencyName)
            let r = state.GetParameter<double>(RandomSearch.RadiusParameterName)
            let newPoint = RandomSearch.GenerateRandomInSphere currentPoint r area
            let newPointEfficiency = newPoint.GetPerformance(f)
            if newPointEfficiency < currentPointEfficiency then
                state.SetParameter(RandomSearch.CurrentPointName, newPoint)
                state.SetParameter(RandomSearch.CurrentPointEfficiencyName, newPointEfficiency)
            ()

    type SetBestNode = 
        inherit GeneralNode<RealVector, double, RealVector> 
        
        new (nodeId: int) as this = { } then this.NodeId <- nodeId
        
        override this.Initialize(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) = ()
        
        override this.Process(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) =
            state.result <- state.GetParameter<RealVector>(RandomSearch.CurrentPointName)
