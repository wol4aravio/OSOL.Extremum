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
                        RealVector newPoint = null;
                        if (alreadySampledPoints.Count > 0)
                        {
                            newPoint = alreadySampledPoints.First()
                                .MoveBy(gorn.GetContinuousUniformVector(area.ToDictionary(kvp => kvp.Key, kvp => Tuple.Create(-0.1, 0.1))))
                                .Constrain(area);
                        }
                        else
                        {
                            newPoint = gorn.GetContinuousUniformVector(area);
                        }
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

            public static Algorithm<RealVector, double, RealVector> CreateAlgorithm(int maxIteration, double maxTime)
            {
                var nodes = new GeneralNode<RealVector, double, RealVector>[]
                {
                    new SetParametersNode<RealVector, double, RealVector>(nodeId: 0, parameters: new Dictionary<string, object> {{"generate", true}}),
                    new SampleNode(nodeId: 1),
                    new TerminationViaMaxIterations<RealVector, double, RealVector>(nodeId: 2, maxIteration: maxIteration),
                    new TerminationViaMaxTime<RealVector, double, RealVector>(nodeId: 3, maxTime: maxTime),
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

        private static Algorithm<RealVector, double, RealVector> toolReal = DummyRealOptimization.CreateAlgorithm(250, 2.5);
        private static Algorithm<IntervalVector, Interval, IntervalVector> toolInterval = DummyIntervalOptimization.CreateAlgorithm();
        
        private static Func<Dictionary<string, double>, double> fReal = v => v["x"];
        private static Func<Dictionary<string, Interval>, Interval> fInterval = v => v["x"];
        
        private static Area area = new Dictionary<string, Tuple<double, double>>
        {
            {"x", Tuple.Create(-10.0, 10.0)}
        };
        private static double eps = 1e-3;

        private static RealTester testerReal = new RealTester();
        private static IntervalTester testerInterval = new IntervalTester();

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
            Assert.True(testerReal.Check(DummyRealOptimization.CreateAlgorithm(100, 120.0), DummyRealOptimization.CreateAlgorithm(250, 300.0)));
            
            bool madeJson = false;
            try
            {
                toolReal.State.ConvertToJson();
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
            Assert.True(testerInterval.Check(toolInterval));
            
            bool madeJson = false;
            try
            {
                toolInterval.State.ConvertToJson();
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