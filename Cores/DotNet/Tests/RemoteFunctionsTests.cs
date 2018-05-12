using System;
using System.Collections.Generic;
using Xunit;

using OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions;
using OSOL.Extremum.Cores.DotNet.Arithmetics;


namespace OSOL.Extremum.Cores.DotNet.Tests
{
    public class RemoteFunctionsTests
    {
        
        public static string TASKS_LOC = Environment.GetEnvironmentVariable("OSOL_EXTREMUM_TASKS_LOC");
        public static int N = 1000;
        
        [Fact]
        public static void TestRealRemoteFunction()
        {
            var f = new RealRemoteFunction(json: $"{TASKS_LOC}/Dummy/Dummy_3.json", port: 5000, field: "f");
            f.Initialize();
            List<double> results = new List<double>();
            for (int i = 0; i < N; ++i)
            {
                var result = f.Calculate(new Dictionary<string, double>()
                {
                    {"x", 1.0},
                    {"y", 2.0},
                    {"z", 3.0}
                });
                results.Add(result);
            }

            f.Terminate();
            
            Assert.True(results.TrueForAll(_ => _ == 36.0));
        }
        
        [Fact]
        public static void TestIntervalRemoteFunction()
        {
            var f = new IntervalRemoteFunction(json: $"{TASKS_LOC}/Dummy/Dummy_3.json", port: 10000, field: "f");
            f.Initialize();
            List<Interval> results = new List<Interval>();
            for (int i = 0; i < N; ++i)
            {
                var result = f.Calculate(new Dictionary<string, Interval>()
                {
                    {"x", new Interval(1, 2)},
                    {"y", new Interval(2, 3)},
                    {"z", new Interval(3, 4)}
                });
                results.Add(result);
            }

            f.Terminate();
            
            Assert.True(results.TrueForAll(_ => _.EqualsTo(new Interval(36, 70))));
        }
    }
}