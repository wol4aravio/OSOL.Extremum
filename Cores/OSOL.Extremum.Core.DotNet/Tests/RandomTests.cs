using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Dynamic;
using System.Linq;
using Xunit;

using OSOL.Extremum.Core.DotNet.Random;
using OSOL.Extremum.Core.DotNet.Random.Distributions;

namespace OSOL.Extremum.Core.DotNet.Tests
{
    public class RandomTests
    {
        private static double eps = 1e-2;
        private static int N = (int) 1e6;
        private static int seed = 17091992;

        Dictionary<int, double> GetProbability<T>(IEnumerable<T> values, Func<T, int> project)
        {
            List<int> projectedValues = values.Select(project).ToList();
            return projectedValues
                .Distinct()
                .ToDictionary(
                    v => v,
                    v => (double)(projectedValues.Count(_v => _v == v)) / projectedValues.Count());
        }

        double Distance<T>(Dictionary<T, double> prob_1, Dictionary<T, double> prob_2)
        {
            List<T> keys = prob_1.Keys.ToList();
            foreach(T k in prob_2.Keys) 
                if(!prob_2.ContainsKey(k))
                    keys.Add(k);
            return keys
                .Select(k =>
                {
                    double v1 = prob_1.ContainsKey(k) ? prob_1[k] : 0.0;
                    double v2 = prob_1.ContainsKey(k) ? prob_2[k] : 0.0;
                    return Math.Abs(v1 - v2);
                }).Average();
        }

        private static GoRN gorn = new GoRN(seed);

        [Fact]
        void TestGetProbabilityFunction()
        {
            double[] initialValues = new double[] { 0.1, 0.2, 0.5, 2.1, 2.2, 3.4 };
            Func<double, int> project = x => (int) x;
            Assert.Equal(
                GetProbability(initialValues, project),
                new Dictionary<int, double>()
                {
                    {0, 0.5},
                    {2, 1.0 / 3.0},
                    {3, 1.0 / 6.0}
                });
        }

        [Fact]
        void TestDistanceFunction()
        {
            Dictionary<int, double> prob = new Dictionary<int, double>()
            {
                {1, 1.0 / 7.0},
                {2, 3.0 / 7.0},
                {3, 2.0 / 7.0},
                {4, 1.0 / 7.0}
            };
            double numOfDigits = Math.Round(1.0 / (0.1 * eps));
            Dictionary<int, double> probRounded = prob.ToDictionary(kvp => kvp.Key, kvp => Math.Round(numOfDigits * kvp.Value) / numOfDigits);
            Assert.True(Distance(prob, probRounded) < eps);
        }

        [Fact]
        void TestDiscreteUniform()
        {
            Dictionary<int, double> idealProb_x = new Dictionary<int, double>()
            {
                {0, 0.5},
                {1, 0.5}
            };
            Dictionary<int, double> idealProb_y = new Dictionary<int, double>()
            {
                {0, 1.0 / 3.0},
                {1, 1.0 / 3.0},
                {2, 1.0 / 3.0}
            };
            
            Dictionary<string, Tuple<int, int>> prob = new Dictionary<string, Tuple<int, int>>()
            {
                {"x", Tuple.Create(0, 1)},
                {"y", Tuple.Create(0, 2)}
            };
            var samples = new List<Dictionary<string, int>>();
            for (int i = 0; i < N; ++i)
                samples.Add(gorn.GetDiscreteUniformVector(prob));

            var calculated_prob_x = GetProbability(samples.Select(kvp => kvp["x"]), _ => _);
            var calculated_prob_y = GetProbability(samples.Select(kvp => kvp["y"]), _ => _);
            
            Assert.True(Distance(idealProb_x, calculated_prob_x) < eps);
            Assert.True(Distance(idealProb_y, calculated_prob_y) < eps);
        }
        
        [Fact]
        void TestContinuousUniform()
        {
            Dictionary<int, double> idealProb_x = new Dictionary<int, double>()
            {
                {1, 0.25},
                {2, 0.25},
                {3, 0.25},
                {4, 0.25}
            };
            Dictionary<int, double> idealProb_y = new Dictionary<int, double>()
            {
                {1, 0.1},
                {2, 0.1},
                {3, 0.1},
                {4, 0.1},
                {5, 0.1},
                {6, 0.1},
                {7, 0.1},
                {8, 0.1},
                {9, 0.1},
                {10, 0.1}
            };
            
            Dictionary<string, Tuple<double, double>> prob = new Dictionary<string, Tuple<double, double>>()
            {
                {"x", Tuple.Create(0.0, 4.0)},
                {"y", Tuple.Create(0.0, 10.0)}
            };
            var samples = new List<Dictionary<string, double>>();
            for (int i = 0; i < N; ++i)
                samples.Add(gorn.GetContinuousUniformVector(prob));

            Func<double, int> f = x => (int) Math.Ceiling(x);
            var calculated_prob_x = GetProbability(samples.Select(kvp => kvp["x"]), f);
            var calculated_prob_y = GetProbability(samples.Select(kvp => kvp["y"]), f);
            
            Assert.True(Distance(idealProb_x, calculated_prob_x) < eps);
            Assert.True(Distance(idealProb_y, calculated_prob_y) < eps);
        }

        [Fact]
        void TestNormalAndStatistic()
        {
            var mu_sigma_x = Tuple.Create(17.0, 7.0);
            var mu_sigma_y = Tuple.Create(7.0, 17.0);
            var prob = new Dictionary<string, Tuple<double, double>>()
            {
                {"x", mu_sigma_x},
                {"y", mu_sigma_y}
            };

            int maxAttempts = 10;
            bool result = false;
            for (int i = 0; i < maxAttempts && !result; ++i)
            {
                var samples = new List<Dictionary<string, double>>();
                for (int j = 0; j < N; ++j)
                    samples.Add(gorn.GetNormalVector(prob));
                var x = samples.Select(kvp => kvp["x"]);
                var y = samples.Select(kvp => kvp["y"]);

                var muEst_x = Statistics.GetMean(x);
                var sigmaEst_x = Statistics.GetUnbiasedSigma(x);
                var muEst_y = Statistics.GetMean(y);
                var sigmaEst_y = Statistics.GetUnbiasedSigma(y);

                var success_mu_x = Math.Abs(mu_sigma_x.Item1 - muEst_x) < eps;
                var success_mu_y = Math.Abs(mu_sigma_y.Item1 - muEst_y) < eps;
                var success_sigma_x = Math.Abs(mu_sigma_x.Item2 - sigmaEst_x) < eps;
                var success_sigma_y = Math.Abs(mu_sigma_y.Item2 - sigmaEst_y) < eps;

                result = success_mu_x && success_mu_y && success_sigma_x && success_sigma_y;
            }
            Assert.True(result);
        }

        [Fact]
        void TestGetFromSeries()
        {
            int[] elements = new int[] {1, 2, 3};
            int n = 5;
            var chosenWithReturn = new List<int>();
            var chosenWithoutReturn = new List<int>();
            for (int i = 0; i < N / 100; ++i)
            {
                chosenWithoutReturn.AddRange(gorn.GetFromSeries(data: elements.ToList(), n: n, withReturn: false));
                chosenWithReturn.AddRange(gorn.GetFromSeries(data: elements.ToList(), n: n, withReturn: true));
            }
            
            Dictionary<int, double> idealProb = new Dictionary<int, double>()
            {
                {1, 1.0 / 3.0},
                {2, 1.0 / 3.0},
                {3, 1.0 / 3.0}
            };
            
            Assert.True(Distance(GetProbability(chosenWithoutReturn, _ => _), idealProb) < eps);
            Assert.True(Distance(GetProbability(chosenWithReturn, _ => _), idealProb) < eps);
        }

    }
}