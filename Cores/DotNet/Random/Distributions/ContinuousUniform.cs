using System;
using System.Collections.Generic;
using System.Linq;

namespace OSOL.Extremum.Cores.DotNet.Random.Distributions
{
    public interface IContinuousUniform
    {
        double GetContinuousUniform(double min, double max);   
    }

    public static class ContinuousUniformFunctions
    {
        public static Dictionary<string, double> GetContinuousUniformVector(this IContinuousUniform GoRN, Dictionary<string, Tuple<double, double>> area) =>
            area.ToDictionary(kvp => kvp.Key,
                kvp => GoRN.GetContinuousUniform(kvp.Value.Item1, kvp.Value.Item2));
    }
}