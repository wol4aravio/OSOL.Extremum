namespace OSOL.Extremum.Algorithms.FSharp

open OSOL.Extremum.Cores.DotNet.Vectors
open OSOL.Extremum.Cores.DotNet.Optimization
open OSOL.Extremum.Cores.DotNet.Optimization.Testing

open Xunit

module RandomSearchTests = 

    let r: double = 1.0;
    let oneMin: double = 60.0;
    
    [<Fact>]
    let TestRandomSearch() =
        let tester = new RealTester()
        let configs = 
            [|
                RandomSearch.CreateFixedStepRandomSearch (1.0 * r) (1.0 * oneMin)
                RandomSearch.CreateFixedStepRandomSearch (0.5 * r) (2.0 * oneMin)
                RandomSearch.CreateFixedStepRandomSearch (0.1 * r) (5.0 * oneMin)
            |]
        Assert.True(tester.Check configs)