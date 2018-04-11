using System;
using System.Collections.Generic;
using System.Linq;
using Xunit;

using OSOL.Extremum.Core.DotNet.Vectors;

namespace OSOL.Extremum.Core.DotNet.Tests
{
    public class RealVectorTests
    {
        private RealVector v1 = new Dictionary<string, double>(){ {"x", 1.0 }, {"y", 2.0 }, {"z", 3.0 }};
        private RealVector v2 = new Dictionary<string, double>(){ {"x", -1.0 }, {"y", -2.0 }, {"z", -3.0 }};
        private RealVector v3 = new Dictionary<string, double>(){ {"x", -1.0 }, {"z", -3.0 }};
        private RealVector z = new Dictionary<string, double>(){ {"x", 0.0 }, {"y", 0.0 }, {"z", 0.0 }};

        [Fact]
        public void TestKeys()
        {
            Assert.True(v1.Keys.ToArray().Zip(new string[]{"x", "y", "z"}, (first, second) => first.Equals(second)).All(_ => _));
        }

        [Fact]
        public void TestValueExtraction()
        {
            Assert.True(v1["x"] == 1.0);
            Assert.True(v1["y"] == 2.0);
            Assert.True(v1["z", 0.0] == 3.0);
            Assert.True(v1["a", 0.0] == 0.0);
            Assert.Throws<VectorExceptions.MissingKeyException>(() => v1["a"]);
        }

        [Fact]
        public void TestToString()
        {
            Assert.True(v1.ToString().Equals("x -> 1\ny -> 2\nz -> 3"));
        }

        [Fact]
        public void TestAddition()
        {
            Assert.True((RealVector)(v1 + v2) == z);
            Assert.Throws<VectorExceptions.DifferentKeysException>(() => v1 + v3);
        }

        [Fact]
        public void TestAdditionWithImputation()
        {
            RealVector r1 = v1.AddImputeMissingKeys(v3);
            RealVector r2 = new Dictionary<string, double>() {{"x", 0.0}, {"y", 2.0}, {"z", 0.0}};
            Assert.True(r1 == r2);
        }

        [Fact]
        public void TestSubtraction()
        {
            Assert.True((RealVector)(z - v1) == v2);
            Assert.Throws<VectorExceptions.DifferentKeysException>(() => v1 - v3);
        }

        [Fact]
        public void TestSubtractionWithImputation()
        {
            RealVector r1 = v1.SubtractImputeMissingKeys(v3);
            RealVector r2 = new Dictionary<string, double>() {{"x", 2.0}, {"y", 2.0}, {"z", 6.0}};
            Assert.True(r1 == r2);
        }
        

        [Fact]
        public void TestMultiplication()
        {
            Assert.True((RealVector)(v1 * v1) == (RealVector)(v2 * v2));
            Assert.True((RealVector)(v1 * v2) == (RealVector)((RealVector)(-v1) * v1));
            Assert.Throws<VectorExceptions.DifferentKeysException>(() => v1 * v3);
        }

        [Fact]
        public void TestMultiplicationWithImputation()
        {
            RealVector r1 = v1.MultiplyImputeMissingKeys(v3);
            RealVector r2 = new Dictionary<string, double>() {{"x", -1.0}, {"y", 2.0}, {"z", -9.0}};
            Assert.True(r1 == r2);
        }

        [Fact]
        public void TestMultiplyByCoefficient()
        {
            Assert.True((RealVector)( v1 + v1) == (RealVector)(v1 * 2));
        }

        [Fact]
        public void TestMoveBy()
        {
            RealVector r1 = v1
                .MoveBy(new Dictionary<string, double>(){{"x", -1.0}})
                .MoveBy(new Dictionary<string, double>(){{"z", -3.0}, {"y", -2.0}});
            Assert.True(r1 == z);
        }

        [Fact]
        public void TestConstrain()
        {
            RealVector r1 = v1
                .Constrain(new Dictionary<string, Tuple<double, double>>() {{"x", Tuple.Create(-1.0, 0.0)}})
                .Constrain(new Dictionary<string, Tuple<double, double>>() {{"y", Tuple.Create(3.0, 10.0)}})
                .Constrain(new Dictionary<string, Tuple<double, double>>() {{"z", Tuple.Create(-5.0, 5.0)}});
            RealVector r2 = new Dictionary<string, double>() {{"x", 0.0}, {"y", 3.0}, {"z", 3.0}};
            Assert.True(r1 == r2);
        }

        [Fact]
        public void TestGetPerformance()
        {
            Func<Dictionary<string, double>, double> f = v => v["x"] + v["y"] + v["z"];
            Assert.Equal(v1.GetPerformance(f), 6.0);
            Assert.Equal(((RealVector)(v1 * 2.0)).GetPerformance(f), 12.0);
        }

        [Fact]
        public void TestToDoubleValuedVector()
        {
            Assert.Equal(v1.ToBasicForm()["x"], 1.0);
            Assert.Equal(v1.ToBasicForm()["y"], 2.0);
            Assert.Equal(v1.ToBasicForm()["z"], 3.0);
        }

        [Fact]
        public void TestJSON()
        {
            Assert.True(new RealVector(v1.ConvertToJson()) == v1);
            Assert.True(new RealVector(v2.ConvertToJson()) == v2);
            Assert.True(new RealVector(v3.ConvertToJson()) == v3);
        }

    }
}