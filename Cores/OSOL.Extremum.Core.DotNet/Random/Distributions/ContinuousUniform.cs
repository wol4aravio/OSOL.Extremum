using System;
using System.Collections.Generic;
using System.Linq;

namespace OSOL.Extremum.Core.DotNet.Random.Distributions
{
    public interface ContinuousUniform
    {
        double getContinuousUniform(double min, double max);   
    }

    public static class ContinuousUniformFunctions
    {
        public static Dictionary<string, double> Diameter(this ContinuousUniform GoRN, Dictionary<string, Tuple<double, double>> area) =>
            area.ToDictionary(kvp => kvp.Key,
                kvp => GoRN.getContinuousUniform(kvp.Value.Item1, kvp.Value.Item2));
    }
}