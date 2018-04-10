using System;
using OSOL.Extremum.Core.DotNet.Random.Distributions;

namespace OSOL.Extremum.Core.DotNet.Random
{
    public static class GoRN
    {
        private class Core: DiscreteUniform, ContinuousUniform, Normal
        {
            private System.Random _seed;

            public Core(int seed)
            {
                this._seed = new System.Random(seed);
            }

            public Core()
            {
                this._seed = new System.Random();
            }

            public int getDiscreteUniform(int min, int max) => _seed.Next(min, max + 1);

            public double getContinuousUniform(double min, double max) => min + _seed.NextDouble() * (max - min);

            public double getNormal(double mu, double sigma)
            {
                double x = getContinuousUniform(-1.0, 1.0);
                double y = getContinuousUniform(-1.0, 1.0);
                double s = x * x + y * y;

                while (s > 1)
                {
                    x = getContinuousUniform(-1.0, 1.0);
                    y = getContinuousUniform(-1.0, 1.0);
                    s = x * x + y * y;
                }

                double z = x * Math.Sqrt(-2 * Math.Log(s) / s);
                return mu + sigma * z;
            }
        }
        
        private static Core _core = new Core();
    }
}