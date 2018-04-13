using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Core.DotNet.Vectors;
using OSOL.Extremum.Core.DotNet.Optimization;

using Xunit;

namespace OSOL.Extremum.Core.DotNet.Tests
{
    public static class RandomSearchTests
    {
        private static double eps = 1e-3;
        private static double r = 1.0;
        private static double fiveSec = 5.0;

        private static double GetNorm(RealVector v) => Math.Sqrt(v.Elements.Values.Select(x => x * x).Sum());

        [Fact]
        static void Test_1()
        {
            Func<Dictionary<string, double>, double> f1 = v => v["x"] * v["x"];
            var a1 = new[] {"x"}.ToDictionary(v => v, v => Tuple.Create(-10.0, 10.0));
            var tool = RandomSearch.CreateFixedStepRandomSearch(radius: r, maxTime: fiveSec);
            var r1 = tool.Work(f1, a1);
            Assert.True(GetNorm(r1) <= eps);
        }

        [Fact]
        static void Test_2()
        {
            Func<Dictionary<string, double>, double> f2 = v => v["x"] * v["x"] + v["y"] * v["y"];
            var a2 = new[] {"x", "y"}.ToDictionary(v => v, v => Tuple.Create(-10.0, 10.0));
            var tool = RandomSearch.CreateFixedStepRandomSearch(radius: r, maxTime: fiveSec);
            var r2 = tool.Work(f2, a2);
            Assert.True(GetNorm(r2) <= eps);
        }

        [Fact]
        static void Test_3()
        {
            Func<Dictionary<string, double>, double> f3 = v => v["x"] * v["x"] + v["y"] * v["y"] + v["z"] * v["z"];
            var a3 = new[] {"x", "y", "z"}.ToDictionary(v => v, v => Tuple.Create(-10.0, 10.0));
            var tool = RandomSearch.CreateFixedStepRandomSearch(radius: r, maxTime: fiveSec);
            var r3 = tool.Work(f3, a3);
            Assert.True(GetNorm(r3) <= eps);
        }
    }
}