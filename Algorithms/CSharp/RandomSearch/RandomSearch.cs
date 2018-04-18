using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Cores.DotNet.Optimization;
using OSOL.Extremum.Cores.DotNet.Vectors;
using OSOL.Extremum.Cores.DotNet.Optimization.Nodes;
using OSOL.Extremum.Cores.DotNet.Random;
using OSOL.Extremum.Cores.DotNet.Random.Distributions;

namespace OSOL.Extremum.Algorithms.CSharp
{
    
    using Area = Dictionary<string, Tuple<double, double>>;
    
    public static class RandomSearch
    {
        private static string currentPointName = "currentPoint";
        private static string currentPointEfficiencyName = "currentPointEfficiency";
        private static string radiusParameterName = "r";
        private static GoRN gorn = new GoRN();

        private static RealVector GenerateRandomInSpere(RealVector currentPoint, double radius, Area area)
        {
            RealVector normallyDistributed = gorn.GetNormalVector(area.ToDictionary(kvp => kvp.Key, kvp => Tuple.Create(0.0, 1.0)));
            var r = Math.Sqrt(normallyDistributed.Elements.Values.Select(v => v * v).Sum());
            RealVector generatedPoint = (currentPoint +
                                         (RealVector) (normallyDistributed *
                                                       (gorn.GetContinuousUniform(-1.0, 1.0) / r)));
            return generatedPoint.Constrain(area);
        }

        private class GenerateInitialPointNode : GeneralNode<RealVector, double, RealVector>
        {

            public GenerateInitialPointNode(int nodeId)
            {
                this.NodeId = nodeId;
            }
            
            public override void Initialize(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                RealVector initialPoint = gorn.GetContinuousUniformVector(area);
                state.SetParameter(currentPointName, initialPoint);
                state.SetParameter(currentPointEfficiencyName, initialPoint.GetPerformance(f));
            }

            public override void Process(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                
            }
        }

        private class SampleNewPointNode_FixedStep : GeneralNode<RealVector, double, RealVector>
        {
            public SampleNewPointNode_FixedStep(int nodeId)
            {
                this.NodeId = nodeId;
            }

            public override void Initialize(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                
            }

            public override void Process(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                var currentPoint = state.GetParameter<RealVector>(currentPointName);
                var currentPointEfficiency = state.GetParameter<double>(currentPointEfficiencyName);
                var r = state.GetParameter<double>(radiusParameterName);

                var newPoint = GenerateRandomInSpere(currentPoint, r, area);
                var newPointEfficiency = newPoint.GetPerformance(f);

                if (newPointEfficiency < currentPointEfficiency)
                {
                    state.SetParameter(currentPointName, newPoint);
                    state.SetParameter(currentPointEfficiencyName, newPointEfficiency);
                }
            }
        }
        
        private class SetBestNode : GeneralNode<RealVector, double, RealVector>
        {
            public SetBestNode(int nodeId)
            {
                this.NodeId = nodeId;
            }

            public override void Initialize(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                
            }

            public override void Process(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                state.result = state.GetParameter<RealVector>(currentPointName);
            }
        }

        public static Algorithm<RealVector, double, RealVector> CreateFixedStepRandomSearch(double radius, double maxTime)
        {
            var FixedStep_nodes = new GeneralNode<RealVector, double, RealVector>[]
            {
                new SetParametersNode<RealVector, double, RealVector>(nodeId: 0, parameters: new Dictionary<string, object> {{radiusParameterName, radius}}),
                new GenerateInitialPointNode(nodeId: 1),
                new TerminationViaMaxTime<RealVector, double, RealVector>(nodeId: 2, maxTime: maxTime),
                new SampleNewPointNode_FixedStep(nodeId: 3),
                new SetBestNode(nodeId: 4)
            };
            var FixedStep_transitionMatrix = new[]
            {
                Tuple.Create<int, int?, int>(0, null, 1),
                Tuple.Create<int, int?, int>(1, null, 2),
                Tuple.Create<int, int?, int>(2, 0, 3),
                Tuple.Create<int, int?, int>(2, 1, 4),
                Tuple.Create<int, int?, int>(3, null, 2)
            };
            
            return new Algorithm<RealVector, double, RealVector>(FixedStep_nodes, FixedStep_transitionMatrix);
        }
        
    }
}