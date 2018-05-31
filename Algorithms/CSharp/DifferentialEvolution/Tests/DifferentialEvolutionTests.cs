using OSOL.Extremum.Cores.DotNet.Vectors;
using OSOL.Extremum.Cores.DotNet.Optimization;
using OSOL.Extremum.Cores.DotNet.Optimization.Testing;
using Xunit;

namespace OSOL.Extremum.Algorithms.CSharp
{
    public static class DifferentialEvolutionTests
    {
        private static int populationSize = 10;
        private static double weightingFactor = 0.5;
        private static double crossoverRate = 0.75;
        private static double oneMin = 60.0;

        [Fact]
        static void TestRandomSearch()
        {
            var tester = new RealTester();
            Assert.True(tester.Check(
                DifferentialEvolution.CreateDifferentialEvolution(1 * populationSize, weightingFactor, crossoverRate, 1 * oneMin),
                DifferentialEvolution.CreateDifferentialEvolution(5 * populationSize, weightingFactor, crossoverRate, 3 * oneMin),
                DifferentialEvolution.CreateDifferentialEvolution(10 * populationSize, weightingFactor, crossoverRate, 5 * oneMin)));
        }
    }
}