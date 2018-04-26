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

module RandomSearch = 

    let CurrentPointName = "currentPoint"
    let CurrentPointEfficiencyName = "currentPointEfficiency"
    let RadiusParameterName = "r"
    let GoRN = new GoRN()
        
    let GenerateRandomInSphere (currentPoint: RealVector) (radius: double) (area: Dictionary<string, double * double>) =
        let normallyDistributed = area.ToDictionary ((fun kvp -> kvp.Key), (fun kvp -> (0.0, 1.0)))
                                  |> GoRN.GetNormalVector
                                  |> RealVector.op_Implicit
                                  
        let r = normallyDistributed.Elements.Values
                |> Seq.map (fun x -> x * x)
                |> Seq.sum
        
        ((currentPoint + normallyDistributed * (GoRN.GetContinuousUniform(-1.0, 1.0) / r)).Elements |> RealVector.op_Implicit).Constrain area
        
    type GenerateInitialPointNode = 
        inherit GeneralNode<RealVector, double, RealVector> 
        
        new (nodeId: int) as this = { } then this.NodeId <- nodeId
        
        override this.Initialize(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) = 
            let initialPoint: RealVector = GoRN.GetContinuousUniformVector(area) |> RealVector.op_Implicit
            state.SetParameter(CurrentPointName, initialPoint)
            state.SetParameter(CurrentPointEfficiencyName, initialPoint.GetPerformance(f))
            ()
        
        override this.Process(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) = ()
    
    type SampleNewPointNode_FixedStep = 
        inherit GeneralNode<RealVector, double, RealVector>
        
        new (nodeId: int) as this = { } then this.NodeId <- nodeId
        
        override this.Initialize(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) = ()
    
        override this.Process(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) =
            let currentPoint = state.GetParameter<RealVector>(CurrentPointName)
            let currentPointEfficiency = state.GetParameter<Double>(CurrentPointEfficiencyName)
            let r = state.GetParameter<double>(RadiusParameterName)
            let newPoint = GenerateRandomInSphere currentPoint r area
            let newPointEfficiency = newPoint.GetPerformance(f)
            if newPointEfficiency < currentPointEfficiency then
                state.SetParameter(CurrentPointName, newPoint)
                state.SetParameter(CurrentPointEfficiencyName, newPointEfficiency)
            ()
    
    type SetBestNode = 
        inherit GeneralNode<RealVector, double, RealVector> 
        
        new (nodeId: int) as this = { } then this.NodeId <- nodeId
        
        override this.Initialize(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) = ()
        
        override this.Process(f: Func<Dictionary<string, double>, double>, area: Dictionary<string, double * double>, state: State<RealVector, double, RealVector>) =
            state.result <- state.GetParameter<RealVector>(CurrentPointName)
        
    let CreateFixedStepRandomSearch (radius: double) (maxTime: double) =
        let FixedStep_nodes: GeneralNode<RealVector, double, RealVector>[] = 
            [|
                new SetParametersNode<RealVector, double, RealVector>(nodeId = 0, parameters = [|(RadiusParameterName, radius :> obj)|].ToDictionary ((fun kvp -> fst kvp), (fun kvp -> snd kvp)))
                new GenerateInitialPointNode(nodeId = 1)
                new TerminationViaMaxTime<RealVector, double, RealVector>(nodeId = 2, maxTime = maxTime)
                new SampleNewPointNode_FixedStep(nodeId = 3)
                new SetBestNode(nodeId = 4)
            |]
            
        let FixedStep_transitionMatrix: (int * Nullable<int> * int) [] = 
            [|
                (0, new Nullable<int>(), 1)
                (1, new Nullable<int>(), 2)
                (2, new Nullable<int>(0), 3)
                (2, new Nullable<int>(1), 4)
                (3, new Nullable<int>(), 2)
            |]
        
        new Algorithm<RealVector, double, RealVector>(nodes = FixedStep_nodes, transitionMatrix = FixedStep_transitionMatrix)
