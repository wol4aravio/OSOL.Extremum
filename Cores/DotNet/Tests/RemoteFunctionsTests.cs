using System;
using System.Collections.Generic;
using Xunit;

using OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions;
using OSOL.Extremum.Cores.DotNet.Arithmetics;


namespace OSOL.Extremum.Cores.DotNet.Tests
{
    public class RemoteFunctionsTests
    {
        
//        public static string TASKS_LOC = Environment.GetEnvironmentVariable("TASKS_LOC");
        public static string TASKS_LOC = "/Users/wol4aravio/Wol4araVio/Projects/OSOL.Extremum/Tasks";
        
        [Fact]
        public static void TestRealRemoteFunction()
        {
            var f = new RealRemoteFunction(json: $"{TASKS_LOC}/Dummy/Dummy_3.json", port: 5000, field: "f");
            var result = f.Calculate(new Dictionary<string, double>()
            {
                {"x", 1.0}, 
                {"y", 2.0}, 
                {"z", 3.0}
            });
            f.Terminate();
            
            Assert.Equal(result, 36.0);
        }
        
        [Fact]
        public static void TestIntervalRemoteFunction()
        {
            var f = new IntervalRemoteFunction(json: $"{TASKS_LOC}/Dummy/Dummy_3.json", port: 5000, field: "f");
            var result = f.Calculate(new Dictionary<string, Interval>()
            {
                {"x", new Interval(1, 2)},
                {"y", new Interval(2, 3)}, 
                {"z", new Interval(3, 4)}
            });
            f.Terminate();
            
            Assert.True(result.EqualsTo(new Interval(36, 70)));
        }
    }
}