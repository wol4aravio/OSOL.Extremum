using OSOL.Extremum.Core.DotNet.Vectors;
using OSOL.Extremum.Core.DotNet.Optimization;
using OSOL.Extremum.Core.DotNet.Optimization.Testing;
using Xunit;

namespace OSOL.Extremum.Core.DotNet.Tests
{
    public static class RandomSearchTests
    {
        private static double r = 1.0;
        private static double fiveSec = 5.0;

        [Fact]
        static void TestRandomSearch()
        {
            var tester = new RealTester();
            Assert.True(tester.Check(
                RandomSearch.CreateFixedStepRandomSearch(radius: r, maxTime: 1 * fiveSec),
                RandomSearch.CreateFixedStepRandomSearch(radius: r, maxTime: 2 * fiveSec),
                RandomSearch.CreateFixedStepRandomSearch(radius: r, maxTime: 3 * fiveSec)));
        }
    }
}