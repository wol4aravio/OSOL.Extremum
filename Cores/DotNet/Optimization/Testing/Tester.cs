using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions;
using OSOL.Extremum.Cores.DotNet.Vectors;

namespace OSOL.Extremum.Cores.DotNet.Optimization.Testing
{
    public abstract class Tester<TBase, TFuncType, TV> where TV : class, IOptimizable<TBase, TFuncType>
    {
        public RemoteFunction<TFuncType>[] TestFunctions;
        public Dictionary<string, Tuple<double, double>>[] Areas;
        public Dictionary<string, double>[] Solutions;
        public double Tolerance;
        public int Attempts;

        public double Lp_norm(VectorObject<double> v1, VectorObject<double> v2, int p = 2)
        {
            var keys = v1.Keys.ToList();
            foreach (var key in v2.Keys)
            {
                if (!keys.Contains(key))
                {
                    keys.Add(key);
                }
            }
            return keys.Select(k => Math.Pow(Math.Abs(v1[k] - v2[k]), p)).Sum();
        }

        public bool Check(params Algorithm<TBase, TFuncType, TV>[] algorithms)
        {
            bool[] resultsPerFunction = new bool[TestFunctions.Length];
            for (int id = 0; id < TestFunctions.Length; ++id)
            {
                var f = TestFunctions[id];
                var area = Areas[id];
                var sol = Solutions[id];
                bool success = false;
                for (int alg_id = 0; alg_id < algorithms.Length && !success; ++alg_id)
                {
                    var algorithm = algorithms[alg_id];
                    for (int attempt = 0; attempt < Attempts && !success; ++attempt)
                    {
                        algorithm.Reset();
                        f.Initialize();
                        var r = algorithm.Work(f.Calculate, area).ToBasicForm();
                        f.Terminate();
                        success = Lp_norm(r, new RealVector(sol)) < Tolerance;
                    }
                }
                resultsPerFunction[id] = success;
            }

            return resultsPerFunction.All(_ => _);
        }
        
    }
}