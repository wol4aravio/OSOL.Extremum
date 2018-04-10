using System;
using System.Collections.Generic;
using System.Linq;

namespace OSOL.Extremum.Core.DotNet.Random.Distributions
{
    public interface INormal
    {
        double GetNormal(double mu, double sigma);   
    }

    public static class NormalFunctions
    {
        public static Dictionary<string, double> Diameter(this INormal GoRN, Dictionary<string, Tuple<double, double>> area) =>
            area.ToDictionary(kvp => kvp.Key,
                kvp => GoRN.GetNormal(kvp.Value.Item1, kvp.Value.Item2));
    }

}