using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Cores.DotNet.Arithmetics;
using OSOL.Extremum.Cores.DotNet.Cybernatics;
using Xunit;

using OSOL.Extremum.Cores.DotNet.Vectors;

namespace OSOL.Extremum.Cores.DotNet.Tests
{
    public static class CybernaticsTests
    {

        public static Func<VectorObject<double>, VectorObject<double>> HistoryGenerator = v =>
            new RealVector(new Dictionary<string, double>()
            {
                {"x1", 1.0 - Math.Cos(v["t"])},
                {"x2", Math.Sin(v["t"])},
                {"x3", 1.0 + v["t"] - Math.Sin(v["t"]) - Math.Cos(v["t"])}
            });

        public static Func<VectorObject<double>, VectorObject<double>> fRealPure = v =>
            new RealVector(new Dictionary<string, double>()
            {
                {"x1", Math.Sin(v["t"])},
                {"x2", Math.Cos(v["t"])},
                {"x3", v["x1"] + v["x2"]}
            });
        public static Func<VectorObject<double>, VectorObject<double>> uRealPure = v => new RealVector(new Dictionary<string, double>(){});

        public static Func<VectorObject<Interval>, VectorObject<Interval>> fIntervalPure = v =>
            new IntervalVector(new Dictionary<string, Interval>()
            {
                {"x1", v["t"].Sin()},
                {"x2", v["t"].Cos()},
                {"x3", v["x1"] + v["x2"]}
            });
        public static Func<VectorObject<Interval>, VectorObject<Interval>> uIntervalPure = v => new IntervalVector(new Dictionary<string, Interval>(){});

        public static Func<VectorObject<double>, VectorObject<double>> fRealViaControl = v =>
            new RealVector(new Dictionary<string, double>()
            {
                {"x1", Math.Sin(v["u1"])},
                {"x2", Math.Cos(v["u2"])},
                {"x3", v["x1"] + v["x2"]}
            });
        public static Func<VectorObject<double>, VectorObject<double>> uRealViaControl = v => 
            new RealVector(new Dictionary<string, double>()
            {
                {"u1", v["t"]},
                {"u2", v["t"]}
            });

        public static Func<VectorObject<Interval>, VectorObject<Interval>> fIntervalViaControl = v =>
            new IntervalVector(new Dictionary<string, Interval>()
            {
                {"x1", v["u1"].Sin()},
                {"x2", v["u2"].Cos()},
                {"x3", v["x1"] + v["x2"]}
            });
        public static Func<VectorObject<Interval>, VectorObject<Interval>> uIntervalViaControl = v => 
            new IntervalVector(new Dictionary<string, Interval>()
            {
                {"u1", v["t"]},
                {"u2", v["t"]}
            });

        public static int maxSteps = 1000;
        public static double eps = 1e-2;
        public static Dictionary<string, Tuple<double, double>> area = new Dictionary<string, Tuple<double, double>>()
        {
            {"t", Tuple.Create(1.0 - 1e-5, 1.0 + 1e-5)}
        };
        public static double tol = 1e-7;

        [Fact]
        static void TestReal()
        {
            RealVector initialState = new Dictionary<string, double>()
            {
                {"x1", 0.0}, {"x2", 0.0}, {"x3", 0.0}
            };
            var idealStates = new List<RealVector>();
            for (int i = 0; i <= (int) Math.Round(1.0 / eps); ++i)
            {
                idealStates.Add((RealVector)HistoryGenerator(new RealVector(new Dictionary<string, double>(){{"t", i * eps}})));
            }

            var dsRealEuler = new RealValuedDynamicSystem(fRealPure, uRealPure, ButcherTableau.GetEuler());
            var resultRealEuler = dsRealEuler.Simulate(initialState, eps, area, maxSteps, maxOverallError: 1e-7);
            var generatedStatesEuler = resultRealEuler.Item2;
            var averageErrorEuler = generatedStatesEuler.Zip(idealStates, Tuple.Create)
                .Select(pair => (pair.Item1 - pair.Item2).Elements.Select(_ => Math.Abs(_.Value)))
                .Select(_ => _.Average())
                .Average();
            
            var dsRealRK4_Pure = new RealValuedDynamicSystem(fRealPure, uRealPure, ButcherTableau.GetRK4());
            var resultRealRK4_Pure = dsRealRK4_Pure.Simulate(initialState, eps, area, maxSteps, maxOverallError: 1e-7);
            var generatedStatesRK4_Pure = resultRealRK4_Pure.Item2;
            var averageErrorRK4_Pure = generatedStatesRK4_Pure.Zip(idealStates, Tuple.Create)
                .Select(pair => (pair.Item1 - pair.Item2).Elements.Select(_ => Math.Abs(_.Value)))
                .Select(_ => _.Average())
                .Average();
            
            var dsRealRK4_ViaControl = new RealValuedDynamicSystem(fRealViaControl, uRealViaControl, ButcherTableau.GetRK4());
            var resultRealRK4_ViaControl = dsRealRK4_ViaControl.Simulate(initialState, eps, area, maxSteps, maxOverallError: 1e-7);
            var generatedStatesRK4_ViaControl = resultRealRK4_ViaControl.Item2;
            var averageErrorRK4_ViaControl = generatedStatesRK4_ViaControl.Zip(idealStates, Tuple.Create)
                .Select(pair => (pair.Item1 - pair.Item2).Elements.Select(_ => Math.Abs(_.Value)))
                .Select(_ => _.Average())
                .Average();
            
            Assert.True(averageErrorEuler > averageErrorRK4_Pure);
            Assert.True(averageErrorRK4_ViaControl > averageErrorRK4_Pure);
            Assert.True(averageErrorRK4_Pure < tol);
        }
        
        [Fact]
        static void TestInterval()
        {
            IntervalVector initialState = new Dictionary<string, Interval>()
            {
                {"x1", 0.0}, {"x2", 0.0}, {"x3", 0.0}
            };
            var idealStates = new List<IntervalVector>();
            for (int i = 0; i <= (int) Math.Round(1.0 / eps); ++i)
            {
                idealStates.Add(
                    HistoryGenerator(
                        new RealVector(new Dictionary<string, double>(){{"t", i * eps}}))
                        .Elements
                        .ToDictionary(kvp => kvp.Key, kvp => new Interval(kvp.Value)));
            }

            var dsIntervalEuler = new IntervalValuedDynamicSystem(fIntervalPure, uIntervalPure, ButcherTableau.GetEuler());
            var resultIntervalEuler = dsIntervalEuler.Simulate(initialState, eps, area, maxSteps, maxOverallError: 1e-7);
            var generatedStatesEuler = resultIntervalEuler.Item2;
            var averageErrorEuler = generatedStatesEuler.Zip(idealStates, Tuple.Create)
                .Select(pair => (pair.Item1 - pair.Item2).Elements.Select(_ => Math.Abs(_.Value.MiddlePoint) + _.Value.Width))
                .Select(_ => _.Average())
                .Average();
            
            var dsIntervalRK4_Pure = new IntervalValuedDynamicSystem(fIntervalPure, uIntervalPure, ButcherTableau.GetRK4());
            var resultIntervalRK4_Pure = dsIntervalRK4_Pure.Simulate(initialState, eps, area, maxSteps, maxOverallError: 1e-7);
            var generatedStatesRK4_Pure = resultIntervalRK4_Pure.Item2;
            var averageErrorRK4_Pure = generatedStatesRK4_Pure.Zip(idealStates, Tuple.Create)
                .Select(pair => (pair.Item1 - pair.Item2).Elements.Select(_ => Math.Abs(_.Value.MiddlePoint) + _.Value.Width))
                .Select(_ => _.Average())
                .Average();
            
            var dsIntervalRK4_ViaControl = new IntervalValuedDynamicSystem(fIntervalViaControl, uIntervalViaControl, ButcherTableau.GetRK4());
            var resultIntervalRK4_ViaControl = dsIntervalRK4_ViaControl.Simulate(initialState, eps, area, maxSteps, maxOverallError: 1e-7);
            var generatedStatesRK4_ViaControl = resultIntervalRK4_ViaControl.Item2;
            var averageErrorRK4_ViaControl = generatedStatesRK4_ViaControl.Zip(idealStates, Tuple.Create)
                .Select(pair => (pair.Item1 - pair.Item2).Elements.Select(_ => Math.Abs(_.Value.MiddlePoint) + _.Value.Width))
                .Select(_ => _.Average())
                .Average();
            
            Assert.True(averageErrorEuler > averageErrorRK4_Pure);
            Assert.True(averageErrorRK4_ViaControl > averageErrorRK4_Pure);
            Assert.True(averageErrorRK4_Pure < tol);
        }
        
    }
}