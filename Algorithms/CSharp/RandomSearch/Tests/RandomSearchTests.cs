using OSOL.Extremum.Cores.DotNet.Vectors;
using OSOL.Extremum.Cores.DotNet.Optimization;
using OSOL.Extremum.Cores.DotNet.Optimization.Testing;
using Xunit;

namespace OSOL.Extremum.Algorithms.CSharp
{
    public static class RandomSearchTests
    {
        private static double r = 1.0;
        private static double oneMin = 60.0;

        [Fact]
        static void TestRandomSearch()
        {
            var tester = new RealTester();
            Assert.True(tester.Check(
                RandomSearch.CreateFixedStepRandomSearch(radius: (1.0 * r), maxTime: 1 * oneMin),
                RandomSearch.CreateFixedStepRandomSearch(radius: (0.5 * r), maxTime: 2 * oneMin),
                RandomSearch.CreateFixedStepRandomSearch(radius: (0.1 * r), maxTime: 5 * oneMin)));
        }
    }
}