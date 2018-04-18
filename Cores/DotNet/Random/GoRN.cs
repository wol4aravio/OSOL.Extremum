using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.VisualStudio.TestPlatform.TestHost;
using OSOL.Extremum.Cores.DotNet.Random.Distributions;

namespace OSOL.Extremum.Cores.DotNet.Random
{
    public class GoRN : IDiscreteUniform, IContinuousUniform, INormal
    {
        private readonly System.Random _seed;

        public GoRN(int seed)
        {
            this._seed = new System.Random(seed);
        }

        public GoRN()
        {
            this._seed = new System.Random();
        }

        public int GetDiscreteUniform(int min, int max) => _seed.Next(min, max + 1);

        public double GetContinuousUniform(double min, double max) => min + _seed.NextDouble() * (max - min);

        public double GetNormal(double mu, double sigma)
        {
            double x = GetContinuousUniform(-1.0, 1.0);
            double y = GetContinuousUniform(-1.0, 1.0);
            double s = x * x + y * y;

            while (s > 1)
            {
                x = GetContinuousUniform(-1.0, 1.0);
                y = GetContinuousUniform(-1.0, 1.0);
                s = x * x + y * y;
            }

            double z = x * Math.Sqrt(-2 * Math.Log(s) / s);
            return mu + sigma * z;
        }

        public List<T> GetFromSeries<T>(List<T> data, int n, bool withReturn)
        {
            var seq = new List<T>();
            int size = data.Count();
            if (withReturn)
            {
                for (int i = 0; i < n; ++i)
                {
                    seq.Add(data[GetDiscreteUniform(0, size - 1)]);
                }
            }
            else
            {
                seq.AddRange(
                    data
                        .Select(v => Tuple.Create(v, GetContinuousUniform(0.0, 1.0)))
                        .OrderBy(_ => _.Item2)
                        .Select(_ => _.Item1)
                        .Take(n));
            }

            return seq;
        }

    }

}