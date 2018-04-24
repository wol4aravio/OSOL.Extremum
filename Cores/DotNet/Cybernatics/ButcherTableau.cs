using System;
using System.Collections.Generic;

namespace OSOL.Extremum.Cores.DotNet.Cybernatics
{
    public class ButcherTableau
    {
        private Dictionary<Tuple<int, int>, double> A;
        private Dictionary<int, double> B, C;

        public int numberOfParts
        {
            get => B.Count;
        }

        public double GetA(int i, int j) => A.GetValueOrDefault(Tuple.Create(i, j), 0.0);
        public double GetB(int i) => B.GetValueOrDefault(i, 0.0);
        public double GetC(int i) => C.GetValueOrDefault(i, 0.0);

        private ButcherTableau(Dictionary<Tuple<int, int>, double> a, Dictionary<int, double> b, Dictionary<int, double> c)
        {
            this.A = a;
            this.B = b;
            this.C = c;
        }

        public ButcherTableau GetEuler()
        {
            return new ButcherTableau
            (
                a: new Dictionary<Tuple<int, int>, double>(),
                b: new Dictionary<int, double>() {{1, 1.0}},
                c: new Dictionary<int, double>()
            );
        }

        public ButcherTableau GetRK4()
        {
            return new ButcherTableau
            (
                a: new Dictionary<Tuple<int, int>, double>()
                {
                    {Tuple.Create(2, 1), 0.5},
                    {Tuple.Create(3, 2), 0.5},
                    {Tuple.Create(4, 3), 1.0}
                },
                b: new Dictionary<int, double>() {{1, 1.0 / 6.0}, {2, 1.0 / 3.0}, {3, 1.0 / 3.0}, {4, 1.0 / 6.0}},
                c: new Dictionary<int, double>() {{2, 0.5}, {3, 0.5}, {4, 1.0}}
            );
        }


    }
}