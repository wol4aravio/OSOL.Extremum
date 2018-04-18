using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Core.DotNet.Arithmetics;
using OSOL.Extremum.Core.DotNet.Vectors;

namespace OSOL.Extremum.Core.DotNet.Optimization.Testing
{
    public class IntervalTester: Tester<IntervalVector, Interval, IntervalVector>
    {

        public IntervalTester()
        {
            this.Tolerance = 1e-3;
            this.Attempts = 5;

            var vars_1 = new[] {"x"};
            var vars_2 = new[] {"x", "y"};
            var vars_3 = new[] {"x", "y", "z"};
            
            Func<Dictionary<string, Interval >, Interval> f1 = v => v["x"].Power(2.0);
            Dictionary<string, Tuple<double, double>> a1 = vars_1.ToDictionary(k => k, k => Tuple.Create(-10.0, 10.0));
            Dictionary<string, double> s1 = vars_1.ToDictionary(k => k, k => 0.0);
            
            Func<Dictionary<string, Interval >, Interval> f2 = v => v["x"].Power(2.0) + v["y"].Power(2.0);
            Dictionary<string, Tuple<double, double>> a2 = vars_1.ToDictionary(k => k, k => Tuple.Create(-10.0, 10.0));
            Dictionary<string, double> s2 = vars_2.ToDictionary(k => k, k => 0.0);
            
            Func<Dictionary<string, Interval >, Interval> f3 = v => v["x"].Power(2.0) + v["y"].Power(2.0) + v["z"].Power(2.0);
            Dictionary<string, Tuple<double, double>> a3 = vars_1.ToDictionary(k => k, k => Tuple.Create(-10.0, 10.0));
            Dictionary<string, double> s3 = vars_3.ToDictionary(k => k, k => 0.0);

            this.TestFunctions = new[] {f1, f2, f3};
            this.Areas = new[] {a1, a2, a3};
            this.Solutions = new[] {s1, s2, s3};

        }
        
    }
}