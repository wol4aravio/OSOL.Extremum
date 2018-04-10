using System.Collections.Generic;
using System.Linq;
using Xunit;

using OSOL.Extremum.Core.DotNet.Vectors;
using OSOL.Extremum.Core.DotNet.Arithmetics;

namespace OSOL.Extremum.Core.DotNet.Tests
{
    public class IntervalVectorTests
    {
        private IntervalVector v1 = new Dictionary<string, Interval>()
        {
            {"x", 1.0 }, 
            {"y", new Interval(2.0, 3.0)},
            {"z", new Interval(3.0, 5.0)}
        };
        private IntervalVector v2 = new Dictionary<string, Interval>()
        {
            {"x", 1.0 }, 
            {"z", new Interval(-3.0, -2.0)}
        };

        [Fact]
        public void TestKeys()
        {
            Assert.True(v1.Keys.ToArray().Zip(new string[]{"x", "y", "z"}, (first, second) => first.Equals(second)).All(_ => _));
        }

        [Fact]
        public void TestValueExtraction()
        {
            Assert.True(v1["x"] == 1.0);
            Assert.True(v1["y"] == new Interval(2.0, 3.0));
            Assert.True(v1["z", 0.0] == new Interval(3.0, 5.0));
            Assert.True(v1["a", 0.0] == 0.0);
            Assert.Throws<VectorExceptions.MissingKeyException>(() => v1["a"]);
        }

        [Fact]
        public void TestToString()
        {
            Assert.True(v1.ToString().Equals("x -> [1; 1]\ny -> [2; 3]\nz -> [3; 5]"));
        }

        [Fact]
        public void TestAddition()
        {
            Assert.True((IntervalVector)(v1 + v1) == (IntervalVector)(v1 * 2.0));
            Assert.Throws<VectorExceptions.DifferentKeysException>(() => v1 + v2);
        }

        [Fact]
        public void TestAdditionWithImputation()
        {
            IntervalVector r1 = v1.AddImputeMissingKeys(v2);
            IntervalVector r2 = new Dictionary<string, Interval>()
            {
                {"x", 2.0}, 
                {"y", v1["y"]}, 
                {"z", new Interval(0.0, 3.0)}
            };
            Assert.True(r1 == r2);
        }

        [Fact]
        public void TestSubtraction()
        {
            IntervalVector r1 = v1 - v1;
            IntervalVector r2 = new Dictionary<string, Interval>()
            {
                {"x", 0.0}, 
                {"y", new Interval(-1.0, 1.0)}, 
                {"z", new Interval(-2.0, 2.0)}
            };
            Assert.True(r1 == r2);
        }

        [Fact]
        public void TestSubtractionWithImputation()
        {
            IntervalVector r1 = v1.SubtractImputeMissingKeys(v2);
            IntervalVector r2 = new Dictionary<string, Interval>()
            {
                {"x", 0.0}, 
                {"y", v1["y"]}, 
                {"z", new Interval(5.0, 8.0)}
            };
            Assert.True(r1 == r2);
        }
        

        [Fact]
        public void TestMultiplication()
        {
            IntervalVector r1 = v1 * v1;
            IntervalVector r2 = new Dictionary<string, Interval>()
            {
                {"x", 1.0}, 
                {"y", new Interval(4.0, 9.0)}, 
                {"z", new Interval(9.0, 25.0)}
            };
            Assert.True(r1 == r2);
        }

        [Fact]
        public void TestMultiplicationWithImputation()
        {
            IntervalVector r1 = v1.MultiplyImputeMissingKeys(v2);
            IntervalVector r2 = new Dictionary<string, Interval>()
            {
                {"x", 1.0}, 
                {"y", v1["y"]}, 
                {"z", new Interval(-15.0, -6.0)}
            };
            Assert.True(r1 == r2);
        }

        [Fact]
        public void TestMultiplyByCoefficient()
        {
            Assert.True((IntervalVector)((IntervalVector)(v1 + v1) + v1) == (IntervalVector)(v1 * 3.0));
        }

    }
}