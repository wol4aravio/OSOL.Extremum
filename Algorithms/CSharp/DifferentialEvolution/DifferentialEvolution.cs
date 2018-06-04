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
    
    public static class DifferentialEvolution
    {
        private static string populationSizeName = "populationSize";
        private static string populationName = "population";
        private static string populationEfficiencyName = "populationEfficiency";
        private static string bestName = "best";
        private static string weightingFactorName = "weightingFactor";
        private static string crossoverRateName = "crossoverRate";
        private static GoRN gorn = new GoRN();
        
        private class InitializePopulationNode : GeneralNode<RealVector, double, RealVector>
        {

            public InitializePopulationNode(int nodeId)
            {
                this.NodeId = nodeId;
            }
            
            public override void Initialize(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                var populationSize = state.GetParameter<int>(populationSizeName);
                var population = new RealVector[populationSize];

                for (int i = 0; i < populationSize; ++i)
                {
                    RealVector x = gorn.GetContinuousUniformVector(area);
                    population[i] = x;
                }
                    
                state.SetParameter(populationName, population);
            }

            public override void Process(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                
            }
        }

        private class EvaluatePopulationNode : GeneralNode<RealVector, double, RealVector>
        {

            public EvaluatePopulationNode(int nodeId)
            {
                this.NodeId = nodeId;
            }
            
            public override void Initialize(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                
            }

            public override void Process(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                var population = state.GetParameter<RealVector[]>(populationName);
                
                double[] populationEfficiency = population.Select(_ => _.GetPerformance(f)).ToArray();
                state.SetParameter(populationEfficiencyName, populationEfficiency);

                var best = population.Zip(populationEfficiency, Tuple.Create).OrderBy(pair => pair.Item2).First().Item1;
                state.SetParameter(bestName, best);
            }
        }

        private class GenerateNewPopulationNode : GeneralNode<RealVector, double, RealVector>
        {

            public GenerateNewPopulationNode(int nodeId)
            {
                this.NodeId = nodeId;
            }

            public RealVector GenerateNewMember(int initialMemberId, RealVector[] population, double weightingFactor, double crossoverRate)
            {
                List<int> possibleIds = new List<int>();
                for (int i = 0; i < population.Length; ++i)
                {
                    if (i != initialMemberId)
                    {
                        possibleIds.Add(i);
                    }
                }

                var tripletId = gorn.GetFromSeries(possibleIds, 3, false);
                var member_1 = population[tripletId[0]];
                var member_2 = population[tripletId[1]];
                var member_3 = population[tripletId[2]];                

                int dim = population[initialMemberId].Elements.Count;
                string cutPoint = gorn.GetFromSeries(population[initialMemberId].Keys.ToList(), 1, false).First();

                RealVector newMember = population[initialMemberId].Keys
                    .ToDictionary(key => key, key =>
                    {
                        if (string.Equals(cutPoint, key) || gorn.GetContinuousUniform(0.0, 1.0) < crossoverRate)
                        {
                            return member_3[key] + weightingFactor * (member_1[key] - member_2[key]);
                        }
                        else
                        {
                            return population[initialMemberId][key];
                        }
                    });

                return newMember;
            }
            
            public override void Initialize(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                
            }

            public override void Process(Func<Dictionary<string, double>, double> f, Area area, State<RealVector, double, RealVector> state)
            {
                var population = state.GetParameter<RealVector[]>(populationName);
                var populationEfficiency = state.GetParameter<double[]>(populationEfficiencyName);
                var best = state.GetParameter<RealVector>(bestName);
                var weightingFactor = state.GetParameter<double>(weightingFactorName);
                var crossoverRate = state.GetParameter<double>(crossoverRateName);
                
                var populationSize = state.GetParameter<int>(populationSizeName);
                RealVector[] newPopulation = new RealVector[populationSize];

                for (int i = 0; i < populationSize; ++i)
                {
                    var newMember = GenerateNewMember(i, population, weightingFactor, crossoverRate);
                    var newMemberEfficiency = newMember.GetPerformance(f);
                    if (newMemberEfficiency < populationEfficiency[i])
                    {
                        newPopulation[i] = newMember;
                    }
                    else
                    {
                        newPopulation[i] = population[i];
                    }
                }
                
                state.SetParameter(populationName, newPopulation);
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
                state.result = state.GetParameter<RealVector>(bestName);
            }
        }
        
        public static Algorithm<RealVector, double, RealVector> CreateDifferentialEvolution(int populationSize, double weightingFactor, double crossoverRate, double maxTime)
        {
            var DifferentialEvolution_nodes = new GeneralNode<RealVector, double, RealVector>[]
            {
                new SetParametersNode<RealVector, double, RealVector>(
                    nodeId: 0, parameters: 
                    new Dictionary<string, object>
                    {
                        {populationSizeName, populationSize}, 
                        {weightingFactorName, weightingFactor}, 
                        {crossoverRateName, crossoverRate}
                    }),
                new InitializePopulationNode(nodeId: 1),
                new EvaluatePopulationNode(nodeId: 2),
                new TerminationViaMaxTime<RealVector, double, RealVector>(nodeId: 3, maxTime: maxTime),
                new GenerateNewPopulationNode(nodeId: 4),
                new SetBestNode(nodeId: 5)
            };
            var DifferentialEvolution_transitionMatrix = new[]
            {
                Tuple.Create<int, int?, int>(0, null, 1),
                Tuple.Create<int, int?, int>(1, null, 2),
                Tuple.Create<int, int?, int>(2, null, 3),
                Tuple.Create<int, int?, int>(3, 0, 4),
                Tuple.Create<int, int?, int>(3, 1, 5),
                Tuple.Create<int, int?, int>(4, null, 2)
            };
            
            return new Algorithm<RealVector, double, RealVector>(DifferentialEvolution_nodes, DifferentialEvolution_transitionMatrix);
        }
        
    }
}