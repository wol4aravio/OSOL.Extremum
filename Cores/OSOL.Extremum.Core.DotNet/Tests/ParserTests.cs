using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Core.DotNet.Arithmetics;
using Xunit;

using OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser;
using OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser.TreeFunctions;
using OSOL.Extremum.Core.DotNet.Random;
using OSOL.Extremum.Core.DotNet.Random.Distributions;
using OSOL.Extremum.Core.DotNet.Vectors;

namespace OSOL.Extremum.Core.DotNet.Tests
{
    public static class ParserTests
    {
        private static int N = 100;
        private static double tol = 1e-9;
        private static GoRN gorn = new GoRN(17091992);
        private static Dictionary<string, Tuple<double, double>> probability =
            new[] {"x", "y", "z"}.ToDictionary(k => k, k => Tuple.Create(-1.0, 1.0));
        
        private static string str = "-x - 1.0 + (sin(y) + cos(y)) * (exp(-x) + ln(10 - y)) / (abs(-3.0) ** sqrt(4.0))";
        private static Func<Dictionary<string, double>, double> fDouble = v => -v["x"] - 1.0 + (Math.Sin(v["y"])+ Math.Cos(v["y"])) * (Math.Exp(-v["x"]) + Math.Log(10.0 - v["y"])) / Math.Pow(Math.Abs(-3.0), Math.Sqrt(4.0));
        private static Func<Dictionary<string, Interval>, Interval> fInterval = v => -v["x"] - new Interval(1.0) + (v["y"].Sin()+ v["y"].Cos()) * ((-v["x"]).Exp() + (new Interval(10.0) - v["y"]).Ln()) / (new Interval(-3.0).Abs().Power(new Interval(4.0).Sqrt()));

        [Fact]
        public static void TestDoubleTreeFunction()
        {
            var f = new DoubleTreeFunction(str);
            var testPoints = new List<RealVector>();
            for (int i = 0; i < N; ++i)
            {
                testPoints.Add(gorn.GetContinuousUniformVector(probability));
                var asd = fDouble(testPoints.Last().Elements);
                var asdd = f.Calculate(testPoints.Last());
            }
            Assert.True(testPoints.TrueForAll(x => Math.Abs(fDouble(x.Elements) - f.Calculate(x)) < tol));
        }
        
        [Fact]
        public static void TestIntervalTreeFunction()
        {
            var f = new IntervalTreeFunction(str);
            var testPoints = new List<IntervalVector>();
            for (int i = 0; i < N; ++i)
            {
                testPoints.Add(gorn.GetContinuousUniformVector(probability).ToDictionary(kvp => kvp.Key, kvp => new Interval(kvp.Value)));
            }
            Assert.True(testPoints.TrueForAll(x => (fInterval(x.Elements) - f.Calculate(x)).Abs().MiddlePoint < tol));
        }
    }
}