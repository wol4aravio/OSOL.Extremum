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

    public static class IntervalOptimizationTests
    {        
        public static class DummyIntervalOptimization
        {
            private static string ParameterName = "sample";
            
            public class SplitNode: GeneralNode<IntervalVector, Interval, IntervalVector>
            {
                public SplitNode(int nodeId)
                {
                    this.NodeId = nodeId;
                }

                public override void Initialize(Func<Dictionary<string, Interval>, Interval> f, Area area, State<IntervalVector, Interval, IntervalVector> state)
                {
                    state.SetParameter(
                        name: DummyIntervalOptimization.ParameterName, 
                        value: new IntervalVector(area.ToDictionary(_ => _.Key, kvp => new Interval(kvp.Value.Item1, kvp.Value.Item2))));
                }

                public override void Process(Func<Dictionary<string, Interval>, Interval> f, Area area, State<IntervalVector, Interval, IntervalVector> state)
                {
                    var currentIntervalVector = state.GetParameter<IntervalVector>(DummyIntervalOptimization.ParameterName);
                    var leftRight = currentIntervalVector.Bisect();
                    var newIntervalVector = leftRight.Item1;
                    if (leftRight.Item2.GetPerformance(f) < leftRight.Item1.GetPerformance(f))
                    {
                        newIntervalVector = leftRight.Item2;
                    }
                    state.SetParameter(name: DummyIntervalOptimization.ParameterName, value: newIntervalVector);
                }
            }

            public class SelectBest : GeneralNode<IntervalVector, Interval, IntervalVector>
            {
                public SelectBest(int nodeId)
                {
                    this.NodeId = nodeId;
                }

                public override void Initialize(Func<Dictionary<string, Interval>, Interval> f, Area area, State<IntervalVector, Interval, IntervalVector> state)
                {
                }

                public override void Process(Func<Dictionary<string, Interval>, Interval> f, Area area, State<IntervalVector, Interval, IntervalVector> state)
                {
                    state.result = state.GetParameter<IntervalVector>(DummyIntervalOptimization.ParameterName);
                }
            }

            public static Algorithm<IntervalVector, Interval, IntervalVector> CreateAlgorithm()
            {
                var nodes = new GeneralNode<IntervalVector, Interval, IntervalVector>[]
                {
                    new SplitNode(nodeId: 0), 
                    new TerminationViaMaxIterations<IntervalVector, Interval, IntervalVector>(nodeId: 1, maxIteration: 250),
                    new TerminationViaMaxTime<IntervalVector, Interval, IntervalVector>(nodeId: 2, maxTime: 2.5),
                    new SelectBest(nodeId: 3),
                };
                var transitionMatrix = new Tuple<int, int?, int>[]
                {
                    Tuple.Create<int, int?, int>(0, null, 1),
                    Tuple.Create<int, int?, int>(1, 0, 0),
                    Tuple.Create<int, int?, int>(1, 1, 2),
                    Tuple.Create<int, int?, int>(2, 0, 0),
                    Tuple.Create<int, int?, int>(2, 1, 3)                    
                };
                
                return new Algorithm<IntervalVector, Interval, IntervalVector>(nodes, transitionMatrix);
            }
        }

        private static Algorithm<IntervalVector, Interval, IntervalVector> toolInterval = DummyIntervalOptimization.CreateAlgorithm();
        private static IntervalTester testerInterval = new IntervalTester();
        
        [Fact]
        static void TestIntervalOptimization()
        {
            Assert.True(testerInterval.Check(toolInterval));
        }
    }
}