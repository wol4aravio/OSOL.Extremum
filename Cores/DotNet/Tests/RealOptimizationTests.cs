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

    public static class RealOptimizationTests
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
        
        private static RealTester testerReal = new RealTester();

        [Fact]
        static void TestRealOptimization()
        {
            Assert.True(testerReal.Check(DummyRealOptimization.CreateAlgorithm(100, 120.0), DummyRealOptimization.CreateAlgorithm(250, 300.0)));
            System.Threading.Thread.Sleep(5000);
        }

    }
}