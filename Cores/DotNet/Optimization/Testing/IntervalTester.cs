using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Cores.DotNet.Arithmetics;
using OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions;
using OSOL.Extremum.Cores.DotNet.Vectors;

namespace OSOL.Extremum.Cores.DotNet.Optimization.Testing
{
    public class IntervalTester: Tester<IntervalVector, Interval, IntervalVector>
    {
        
        public static string TASKS_LOC = Environment.GetEnvironmentVariable("OSOL_EXTREMUM_TASKS_LOC");

        public IntervalTester()
        {
            this.Tolerance = 1e-3;
            this.Attempts = 5;

            var vars_1 = new[] {"x"};
            var vars_2 = new[] {"x", "y"};
            var vars_3 = new[] {"x", "y", "z"};
            
            RemoteFunction<Interval> f1 = new IntervalRemoteFunction(json: $"{TASKS_LOC}/Dummy/Dummy_1.json", port: 11121, field: "f");
            Dictionary<string, Tuple<double, double>> a1 = vars_1.ToDictionary(k => k, k => Tuple.Create(-10.0, 10.0));
            Dictionary<string, double> s1 = vars_1.ToDictionary(k => k, k => 0.0);
            
            RemoteFunction<Interval> f2 = new IntervalRemoteFunction(json: $"{TASKS_LOC}/Dummy/Dummy_2.json", port: 11122, field: "f");
            Dictionary<string, Tuple<double, double>> a2 = vars_2.ToDictionary(k => k, k => Tuple.Create(-10.0, 10.0));
            Dictionary<string, double> s2 = vars_2.ToDictionary(k => k, k => 0.0);
            
            RemoteFunction<Interval> f3 = new IntervalRemoteFunction(json: $"{TASKS_LOC}/Dummy/Dummy_3.json", port: 11123, field: "f");
            Dictionary<string, Tuple<double, double>> a3 = vars_3.ToDictionary(k => k, k => Tuple.Create(-10.0, 10.0));
            Dictionary<string, double> s3 = vars_3.ToDictionary(k => k, k => 0.0);

            this.TestFunctions = new[] {f1, f2, f3};
            this.Areas = new[] {a1, a2, a3};
            this.Solutions = new[] {s1, s2, s3};

        }
        
    }
}