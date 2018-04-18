using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Core.DotNet.Vectors;

namespace OSOL.Extremum.Core.DotNet.Optimization.Testing
{
    public class RealTester: Tester<RealVector, double, RealVector>
    {

        public RealTester()
        {
            this.Tolerance = 1e-3;
            this.Attempts = 5;

            var vars_1 = new[] {"x"};
            var vars_2 = new[] {"x", "y"};
            var vars_3 = new[] {"x", "y", "z"};
            
            Func<Dictionary<string, double >, double> f1 = v => Math.Pow(v["x"], 2.0);
            Dictionary<string, Tuple<double, double>> a1 = vars_1.ToDictionary(k => k, k => Tuple.Create(-10.0, 10.0));
            Dictionary<string, double> s1 = vars_1.ToDictionary(k => k, k => 0.0);
            
            Func<Dictionary<string, double >, double> f2 = v => Math.Pow(v["x"], 2.0) + Math.Pow(v["y"], 2.0);
            Dictionary<string, Tuple<double, double>> a2 = vars_1.ToDictionary(k => k, k => Tuple.Create(-10.0, 10.0));
            Dictionary<string, double> s2 = vars_2.ToDictionary(k => k, k => 0.0);
            
            Func<Dictionary<string, double >, double> f3 = v => Math.Pow(v["x"], 2.0) + Math.Pow(v["y"], 2.0) + Math.Pow(v["z"], 2.0);
            Dictionary<string, Tuple<double, double>> a3 = vars_1.ToDictionary(k => k, k => Tuple.Create(-10.0, 10.0));
            Dictionary<string, double> s3 = vars_3.ToDictionary(k => k, k => 0.0);

            this.TestFunctions = new[] {f1, f2, f3};
            this.Areas = new[] {a1, a2, a3};
            this.Solutions = new[] {s1, s2, s3};

        }
        
    }
}