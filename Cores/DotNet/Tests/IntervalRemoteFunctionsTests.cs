using System;
using System.Collections.Generic;
using Xunit;

using OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions;
using OSOL.Extremum.Cores.DotNet.Arithmetics;


namespace OSOL.Extremum.Cores.DotNet.Tests
{
    public class IntervalRemoteFunctionsTests
    {
        
        public static string TASKS_LOC = Environment.GetEnvironmentVariable("OSOL_EXTREMUM_TASKS_LOC");
        
        [Fact]
        public static void TestIntervalRemoteFunction()
        {
            var f = new IntervalRemoteFunction(json: $"{TASKS_LOC}/Dummy/Dummy_3.json", port: 5000, field: "f");
            f.Initialize();
            var result = f.Calculate(new Dictionary<string, Interval>()
            {
                {"x", new Interval(1, 2)},
                {"y", new Interval(2, 3)}, 
                {"z", new Interval(3, 4)}
            });
            f.Terminate();
            
            Assert.True(result.EqualsTo(new Interval(36, 70)));
            System.Threading.Thread.Sleep(5000);
        }
    }
}