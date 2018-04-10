using System;
using System.Collections.Generic;
using System.Linq;

namespace OSOL.Extremum.Core.DotNet.Random.Distributions
{
    public interface Normal
    {
        double getNormal(double mu, double sigma);   
    }

    public static class NormalFunctions
    {
        public static Dictionary<string, double> Diameter(this Normal GoRN, Dictionary<string, Tuple<double, double>> area) =>
            area.ToDictionary(kvp => kvp.Key,
                kvp => GoRN.getNormal(kvp.Value.Item1, kvp.Value.Item2));
    }

}