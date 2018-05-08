using System;
using System.Collections.Generic;
using Xunit;

using OSOL.Extremum.Cores.DotNet.Optimization.RemoteFunctions;
using OSOL.Extremum.Cores.DotNet.Arithmetics;


namespace OSOL.Extremum.Cores.DotNet.Tests
{
    public class RealRemoteFunctionsTests
    {
        
        public static string TASKS_LOC = Environment.GetEnvironmentVariable("OSOL_EXTREMUM_TASKS_LOC");
        
        [Fact]
        public static void TestRealRemoteFunction()
        {
            var f = new RealRemoteFunction(json: $"{TASKS_LOC}/Dummy/Dummy_3.json", port: 5000, field: "f");
            f.Initialize();
            var result = f.Calculate(new Dictionary<string, double>()
            {
                {"x", 1.0}, 
                {"y", 2.0}, 
                {"z", 3.0}
            });
            f.Terminate();
            
            Assert.Equal(result, 36.0);
            System.Threading.Thread.Sleep(5000);
        }
        
    }
}