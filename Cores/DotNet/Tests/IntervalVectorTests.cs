using System;
using System.Collections.Generic;
using System.Linq;
using Xunit;

using OSOL.Extremum.Cores.DotNet.Vectors;
using OSOL.Extremum.Cores.DotNet.Arithmetics;

namespace OSOL.Extremum.Cores.DotNet.Tests
{
    public static class IntervalVectorTests
    {
        private static IntervalVector v1 = new Dictionary<string, Interval>
        {
            {"x", 1.0 }, 
            {"y", new Interval(2.0, 3.0)},
            {"z", new Interval(3.0, 5.0)}
        };
        private static IntervalVector v2 = new Dictionary<string, Interval>
        {
            {"x", 1.0 }, 
            {"z", new Interval(-3.0, -2.0)}
        };

        [Fact]
        public static void TestKeys()
        {
            Assert.True(v1.Keys.ToArray().Zip(new []{"x", "y", "z"}, (first, second) => first.Equals(second)).All(_ => _));
        }

        [Fact]
        public static void TestValueExtraction()
        {
            Assert.True(v1["x"] == 1.0);
            Assert.True(v1["y"] == new Interval(2.0, 3.0));
            Assert.True(v1["z", 0.0] == new Interval(3.0, 5.0));
            Assert.True(v1["a", 0.0] == 0.0);
            Assert.Throws<VectorExceptions.MissingKeyException>(() => v1["a"]);
        }

        [Fact]
        public static void TestToString()
        {
            Assert.True(v1.ToString().Equals("x -> [1; 1]\ny -> [2; 3]\nz -> [3; 5]"));
        }

        [Fact]
        public static void TestAddition()
        {
            Assert.True((IntervalVector)(v1 + v1) == (IntervalVector)(v1 * 2.0));
            Assert.Throws<VectorExceptions.DifferentKeysException>(() => v1 + v2);
        }

        [Fact]
        public static void TestAdditionWithImputation()
        {
            IntervalVector r1 = v1.AddImputeMissingKeys(v2);
            IntervalVector r2 = new Dictionary<string, Interval>
            {
                {"x", 2.0}, 
                {"y", v1["y"]}, 
                {"z", new Interval(0.0, 3.0)}
            };
            Assert.True(r1 == r2);
        }

        [Fact]
        public static void TestSubtraction()
        {
            IntervalVector r1 = v1 - v1;
            IntervalVector r2 = new Dictionary<string, Interval>
            {
                {"x", 0.0}, 
                {"y", new Interval(-1.0, 1.0)}, 
                {"z", new Interval(-2.0, 2.0)}
            };
            Assert.True(r1 == r2);
        }

        [Fact]
        public static void TestSubtractionWithImputation()
        {
            IntervalVector r1 = v1.SubtractImputeMissingKeys(v2);
            IntervalVector r2 = new Dictionary<string, Interval>
            {
                {"x", 0.0}, 
                {"y", v1["y"]}, 
                {"z", new Interval(5.0, 8.0)}
            };
            Assert.True(r1 == r2);
        }
        

        [Fact]
        public static void TestMultiplication()
        {
            IntervalVector r1 = v1 * v1;
            IntervalVector r2 = new Dictionary<string, Interval>
            {
                {"x", 1.0}, 
                {"y", new Interval(4.0, 9.0)}, 
                {"z", new Interval(9.0, 25.0)}
            };
            Assert.True(r1 == r2);
        }

        [Fact]
        public static void TestMultiplicationWithImputation()
        {
            IntervalVector r1 = v1.MultiplyImputeMissingKeys(v2);
            IntervalVector r2 = new Dictionary<string, Interval>
            {
                {"x", 1.0}, 
                {"y", v1["y"]}, 
                {"z", new Interval(-15.0, -6.0)}
            };
            Assert.True(r1 == r2);
        }

        [Fact]
        public static void TestMultiplyByCoefficient()
        {
            Assert.True((IntervalVector)((IntervalVector)(v1 + v1) + v1) == (IntervalVector)(v1 * 3.0));
        }

        [Fact]
        public static void TestSplitting_1()
        {
            var result = v1.Bisect();
            IntervalVector r1 = new Dictionary<string, Interval>
            {
                {"x", 1.0}, 
                {"y", new Interval(2.0, 3.0)}, 
                {"z", new Interval(3.0, 4.0)}
            };
            IntervalVector r2 = new Dictionary<string, Interval>
            {
                {"x", 1.0}, 
                {"y", new Interval(2.0, 3.0)}, 
                {"z", new Interval(4.0, 5.0)}
            };
            Assert.True(result.Item1 == r1);
            Assert.True(result.Item2 == r2);
        }
        
        [Fact]
        public static void TestSplitting_2()
        {
            var result = v1.Bisect(key: "y");
            IntervalVector r1 = new Dictionary<string, Interval>
            {
                {"x", 1.0}, 
                {"y", new Interval(2.0, 2.5)}, 
                {"z", new Interval(3.0, 5.0)}
            };
            IntervalVector r2 = new Dictionary<string, Interval>
            {
                {"x", 1.0}, 
                {"y", new Interval(2.5, 3.0)}, 
                {"z", new Interval(3.0, 5.0)}
            };
            Assert.True(result.Item1 == r1);
            Assert.True(result.Item2 == r2);
        }

        [Fact]
        public static void TestJSON()
        {
            Assert.True(new IntervalVector(v1.ConvertToJson()) == v1);
            Assert.True(new IntervalVector(v2.ConvertToJson()) == v2);
        }

        [Fact]
        public static void TestMoveBy()
        {
            IntervalVector r1 = v1
                .MoveBy(new Dictionary<string, double>{{"x", -1.0}})
                .MoveBy(new Dictionary<string, double>{{"z", -3.0}, {"y", -2.0}});
            IntervalVector r2 = new Dictionary<string, Interval>
            {
                {"x", 0.0}, 
                {"y", new Interval(0.0, 1.0)}, 
                {"z", new Interval(0.0, 2.0)}
            };
            Assert.True(r1 == r2);
        }

        [Fact]
        public static void TestConstrain()
        {
            IntervalVector r1 = v1
                .Constrain(new Dictionary<string, Tuple<double, double>> {{"x", Tuple.Create(-1.0, 0.0)}})
                .Constrain(new Dictionary<string, Tuple<double, double>> {{"y", Tuple.Create(3.0, 10.0)}})
                .Constrain(new Dictionary<string, Tuple<double, double>> {{"z", Tuple.Create(-5.0, 4.0)}});
            IntervalVector r2 = new Dictionary<string, Interval>
            {
                {"x", 0.0}, 
                {"y", 3.0}, 
                {"z", new Interval(3.0, 4.0)}
            };
            Assert.True(r1 == r2);
        }

        [Fact]
        public static void TestGetPerformance()
        {
            Func<Dictionary<string, Interval>, Interval> f = v => v["x"] - v["y"] + v["z"];
            Assert.Equal(v1.GetPerformance(f), 1.0);
            Assert.Equal(((IntervalVector)(v1 * 2.0)).GetPerformance(f), 2.0);
        }

        [Fact]
        public static void TestToDoubleValuedVector()
        {
            Assert.Equal(v1.ToBasicForm()["x"], 1.0);
            Assert.Equal(v1.ToBasicForm()["y"], 2.5);
            Assert.Equal(v1.ToBasicForm()["z"], 4.0);
        }

    }
}