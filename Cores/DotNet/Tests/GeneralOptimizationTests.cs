using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Cores.DotNet.Arithmetics;
using Xunit;

using OSOL.Extremum.Cores.DotNet.Vectors;
using OSOL.Extremum.Cores.DotNet.Optimization;
using OSOL.Extremum.Cores.DotNet.Optimization.Nodes;
using OSOL.Extremum.Cores.DotNet.Optimization.Testing;
using OSOL.Extremum.Cores.DotNet.Random;
using OSOL.Extremum.Cores.DotNet.Random.Distributions;

namespace OSOL.Extremum.Cores.DotNet.Tests
{
    
    using Area = Dictionary<string, Tuple<double, double>>;

    public static class GeneralOptimizationTests
    {        
        private static Func<Dictionary<string, double>, double> fReal = v => Math.Abs(v["x"]);
        private static Func<Dictionary<string, Interval>, Interval> fInterval = v => v["x"].Abs();
        
        private static Area area = new Dictionary<string, Tuple<double, double>>
        {
            {"x", Tuple.Create(-10.0, 10.0)}
        };

        [Fact]
        static void TestTerminationViaMaxIterations()
        {
            var node = new TerminationViaMaxIterations<RealVector, double, RealVector>(nodeId: 1, maxIteration: 250);
            var state = new State<RealVector, double, RealVector>();
            
            node.Initialize(fReal, area, state);
            Assert.Throws<OptimizationExceptions.ParameterAlreadyExistsException>(() =>
                node.Initialize(fReal, area, state));
        }

        [Fact]
        static void TestTerminationViaMaxTime()
        {
            var node = new TerminationViaMaxTime<IntervalVector, Interval, IntervalVector>(nodeId: 1, maxTime: 2.5);
            var state = new State<IntervalVector, Interval, IntervalVector>();
            
            node.Initialize(fInterval, area, state);
            Assert.Throws<OptimizationExceptions.ParameterAlreadyExistsException>(() =>
                node.Initialize(fInterval, area, state));
        }

    }
}