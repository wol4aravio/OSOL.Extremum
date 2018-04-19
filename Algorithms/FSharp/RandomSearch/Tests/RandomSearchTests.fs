namespace OSOL.Extremum.Algorithms.FSharp

open OSOL.Extremum.Cores.DotNet.Vectors
open OSOL.Extremum.Cores.DotNet.Optimization
open OSOL.Extremum.Cores.DotNet.Optimization.Testing

open Xunit

module RandomSearchTests = 

    let r: double = 1.0;
    let fiveSec: double = 5.0;
    
    [<Fact>]
    let TestRandomSearch() =
        let tester = new RealTester()
        let configs = 
            [|
                RandomSearch.CreateFixedStepRandomSearch r (1.0 * fiveSec)
                RandomSearch.CreateFixedStepRandomSearch r (2.0 * fiveSec)
                RandomSearch.CreateFixedStepRandomSearch r (3.0 * fiveSec)
            |]
        Assert.True(tester.Check configs)