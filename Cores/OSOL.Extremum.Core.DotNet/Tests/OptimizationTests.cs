using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Core.DotNet.Arithmetics;
using Xunit;

using OSOL.Extremum.Core.DotNet.Vectors;
using OSOL.Extremum.Core.DotNet.Optimization;
using OSOL.Extremum.Core.DotNet.Optimization.Nodes;
using OSOL.Extremum.Core.DotNet.Random;
using OSOL.Extremum.Core.DotNet.Random.Distributions;

namespace OSOL.Extremum.Core.DotNet.Tests
{
    
    using Area = Dictionary<string, Tuple<double, double>>;

    public static class OptimizationTests
    {
        public static class DummyRealOptimization
        {
            private static string ParameterName = "samples";
            private static GoRN gorn = new GoRN();
            
            public class SampleNode: GeneralNode<RealVector, double, RealVector>
            {
                public SampleNode(int nodeId)
                {
                    this.NodeId = nodeId;
                }

                public override void Initialize(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
                {
                    state.SetParameter(name: DummyRealOptimization.ParameterName, value: new List<RealVector>());
                    return;
                }

                public override void Process(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
                {
                    List<RealVector> alreadySampledPoints = state.GetParameter<List<RealVector>>(DummyRealOptimization.ParameterName);
                    if (state.GetParameter<bool>("generate"))
                    {
                        RealVector newPoint = gorn.GetContinuousUniformVector(area);
                        alreadySampledPoints.Add(newPoint);
                        state.SetParameter<List<RealVector>>(name: DummyRealOptimization.ParameterName, value: alreadySampledPoints.OrderBy(_ => _.GetPerformance(f)).Take(9).ToList());
                    }
                }
            }

            public class SelectBest : GeneralNode<RealVector, double, RealVector>
            {
                public SelectBest(int nodeId)
                {
                    this.NodeId = nodeId;
                }

                public override void Initialize(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
                {
                }

                public override void Process(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
                {
                    state.result = state.GetParameter<List<RealVector>>(DummyRealOptimization.ParameterName)
                        .OrderBy(_ => _.GetPerformance(f)).First();
                }
            }

            public static Algorithm<RealVector, double, RealVector> CreateAlgorithm()
            {
                var nodes = new GeneralNode<RealVector, double, RealVector>[]
                {
                    new SetParametersNode<RealVector, double, RealVector>(nodeId: 0, parameters: new Dictionary<string, object>() {{"generate", true}}),
                    new SampleNode(nodeId: 1),
                    new TerminationViaMaxIterations<RealVector, double, RealVector>(nodeId: 2, maxIteration: 250),
                    new TerminationViaMaxTime<RealVector, double, RealVector>(nodeId: 3, maxTime: 2.5),
                    new SelectBest(nodeId: 4),
                };
                var transitionMatrix = new Tuple<int, int?, int>[]
                {
                    Tuple.Create<int, int?, int>(0, null, 1),
                    Tuple.Create<int, int?, int>(1, null, 2),
                    Tuple.Create<int, int?, int>(2, 0, 1),
                    Tuple.Create<int, int?, int>(2, 1, 3),
                    Tuple.Create<int, int?, int>(3, 0, 1),
                    Tuple.Create<int, int?, int>(3, 1, 4)                    
                };
                
                return new Algorithm<RealVector, double, RealVector>(nodes, transitionMatrix);
            }
        }
        
        public static class DummyIntervalOptimization
        {
            private static string ParameterName = "sample";
            private static GoRN gorn = new GoRN();
            
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

        private static Algorithm<RealVector, double, RealVector> toolReal = DummyRealOptimization.CreateAlgorithm();
        private static Algorithm<IntervalVector, Interval, IntervalVector> toolInterval = DummyIntervalOptimization.CreateAlgorithm();
        private static Func<Dictionary<string, double>, double> fReal = v => Math.Abs(v["x"]);
        private static Func<Dictionary<string, Interval>, Interval> fInterval = v => v["x"].Abs();
        private static Area area = new Dictionary<string, Tuple<double, double>>()
        {
            {"x", Tuple.Create(-10.0, 10.0)}
        };
        private static double eps = 1e-3;

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

        [Fact]
        static void TestRealOptimization()
        {
            var result = toolReal.Work(fReal, area);
            Assert.True(Math.Abs(result["x"]) < eps);
            
            bool madeJson = false;
            try
            {
                var json = toolReal.State.ConvertToJson();
                madeJson = true;
            }
            catch (Exception e)
            {
                madeJson = false;
            }
            Assert.True(madeJson);
        }

        [Fact]
        static void TestIntervalOptimization()
        {
            var result = toolInterval.Work(fInterval, area);
            Assert.True(Math.Abs(result["x"].MiddlePoint) < eps);
            
            bool madeJson = false;
            try
            {
                var json = toolInterval.State.ConvertToJson();
                madeJson = true;
            }
            catch (Exception e)
            {
                madeJson = false;
            }
            Assert.True(madeJson);

        }
    }
}