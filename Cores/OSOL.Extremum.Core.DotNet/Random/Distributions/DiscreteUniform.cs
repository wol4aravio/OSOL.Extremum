using System;
using System.Collections.Generic;
using System.Linq;

namespace OSOL.Extremum.Core.DotNet.Random.Distributions
{
    public interface DiscreteUniform
    {
        int getDiscreteUniform(int min, int max);   
    }

    public static class DiscreteUniformFunctions
    {
        public static Dictionary<string, int> Diameter(this DiscreteUniform GoRN, Dictionary<string, Tuple<int, int>> area) =>
            area.ToDictionary(kvp => kvp.Key,
                kvp => GoRN.getDiscreteUniform(kvp.Value.Item1, kvp.Value.Item2));
    }

}