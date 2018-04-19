namespace OSOL.Extremum.Algorithms.FSharp

open System.Collections.Generic
open System.Linq
open System.Linq;
open OSOL.Extremum.Cores.DotNet.Optimization;
open OSOL.Extremum.Cores.DotNet.Vectors;
open OSOL.Extremum.Cores.DotNet.Optimization.Nodes;
open OSOL.Extremum.Cores.DotNet.Random;
open OSOL.Extremum.Cores.DotNet.Random.Distributions;

[<AbstractClass; Sealed>]
type RandomSearch =
    static member currentPointName = "currentPoint"
    static member currentPointEfficiencyName = "currentPointEfficiency"
    static member radiusParameterName = "r"
    static member gorn = new GoRN()
    
    static member generateRandomInSphere (currentPoint: RealVector) (radius: double) (area: Dictionary<string, double * double>) =
        let normallyDistributed = area.ToDictionary ((fun kvp -> kvp.Key), (fun kvp -> (0.0, 1.0)))
                                  |> RandomSearch.gorn.GetNormalVector
                                  |> fun x -> new RealVector(x)
                                  
        let r = normallyDistributed.Elements.Values
                |> Seq.map (fun x -> x * x)
                |> Seq.sum
                
        (currentPoint + new RealVector(normallyDistributed * (RandomSearch.gorn.GetContinuousUniform(-1.0, 1.0) / r)))