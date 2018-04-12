using System;
using Xunit;

using OSOL.Extremum.Core.DotNet.Arithmetics;

namespace OSOL.Extremum.Core.DotNet.Tests
{
    public static class IntervalTests
    {
        static Interval i1 = new Interval(-1.0, 2.0);
        static Interval i2 = new Interval(-4.0, 3.0);
        static Interval i3 = new Interval(1.0, 2.0);
        static Interval i4 = new Interval(5.0, 5.1);
        static Interval i5 = new Interval(-6.0, -5.0);
        static Interval i6 = new Interval(-2.0, 0.0);
        static Interval i7 = new Interval(0.0, 3.0);

        [Fact]
        static void TestBadInitialization()
        {
            Assert.Throws<IntervalExceptions.MinMaxFailureException>(() => new Interval(2.0, -2.0));
        }

        [Fact]
        static void TestToString()
        {
            Assert.True(i1.ToString().Equals("[-1; 2]"));
            Assert.True(i4.ToString().Equals("[5; 5.1]"));
            Assert.True(i7.ToString().Equals("[0; 3]"));
        }

        [Fact]
        static void TestMiddlePoint()
        {
            Assert.Equal(i1.MiddlePoint, 0.5);
            Assert.Equal(i3.MiddlePoint, 1.5);
            Assert.Equal(i7.MiddlePoint, 1.5);
        }

        [Fact]
        static void TestWidth()
        {
            Assert.Equal(i1.Width, 3.0);
            Assert.Equal(i3.Width, 1.0);
            Assert.Equal(i7.Width, 3.0);
        }

        [Fact]
        static void TestRadius()
        {
            Assert.Equal(i1.Radius, 1.5);
            Assert.Equal(i3.Radius, 0.5);
            Assert.Equal(i7.Radius, 1.5);
        }

        [Fact]
        static void TestApproximateEquality()
        {
            Assert.True(i1.ApproximatelyEqualsTo(i1 + 1e-7));
            Assert.False((new Interval(double.NegativeInfinity, 0.0)).ApproximatelyEqualsTo(new Interval(double.NegativeInfinity, double.NaN)));
        }

        [Fact]
        static void TestAddition()
        {
            Assert.True((i1 + i2).ApproximatelyEqualsTo(new Interval(-5.0, 5.0)));
            Assert.True((i2 + i3).ApproximatelyEqualsTo(new Interval(-3.0, 5.0)));
            Assert.True((i5 + i4).ApproximatelyEqualsTo(new Interval(-1.0, 0.1)));
        }

        [Fact]
        static void TestSubtraction()
        {
            Assert.True((i1 - i2).ApproximatelyEqualsTo(new Interval(-4.0, 6.0)));
            Assert.True((i2 - i3).ApproximatelyEqualsTo(new Interval(-6.0, 2.0)));
            Assert.True((i5 - i4).ApproximatelyEqualsTo(new Interval(-11.1, -10.0)));
        }
        
        [Fact]
        static void TestMultiplication()
        {
            Assert.True((i1 * i2).ApproximatelyEqualsTo(new Interval(-8.0, 6.0)));
            Assert.True((i2 * i3).ApproximatelyEqualsTo(new Interval(-8.0, 6.0)));
            Assert.True((i5 * i4).ApproximatelyEqualsTo(new Interval(-30.6, -25.0)));
        }
        
        [Fact]
        static void TestDivision()
        {
            Assert.True((i1 / i2).ApproximatelyEqualsTo(new Interval(double.NegativeInfinity, double.PositiveInfinity)));
            Assert.True((i2 / i3).ApproximatelyEqualsTo(new Interval(-4.0, 3.0)));
            Assert.True((i1 / i5).ApproximatelyEqualsTo(new Interval(-0.4, 0.2)));
            Assert.True((i3 / i6).ApproximatelyEqualsTo(new Interval(double.NegativeInfinity, -0.5)));
            Assert.True((i5 / i7).ApproximatelyEqualsTo(new Interval(double.NegativeInfinity, -5.0 / 3.0)));
        }
        
        [Fact]
        static void TestPower()
        {
            Assert.True((i1.Power(2.0)).ApproximatelyEqualsTo(new Interval(0.0, 4.0)));
            Assert.True((i2.Power(3.0)).ApproximatelyEqualsTo(new Interval(-64.0, 27.0)));
            Assert.True((i5.Power(0.0)).ApproximatelyEqualsTo(new Interval(1.0, 1.0)));
            Assert.Throws<IntervalExceptions.UnknownOperationException>(() => i1.Power(new Interval(-1.0, 1.0)));
        }

        [Fact]
        static void TestNeg()
        {
            Assert.True((-i1).ApproximatelyEqualsTo(new Interval(-2.0, 1.0)));
            Assert.True((-i5).ApproximatelyEqualsTo(new Interval(5.0, 6.0)));
            Assert.True((-i6).ApproximatelyEqualsTo(new Interval(0.0, 2.0)));
        }

        [Fact]
        static void TestSin()
        {
            Assert.True((i1.Sin()).ApproximatelyEqualsTo(new Interval(Math.Sin(-1.0), 1.0)));
            Assert.True((i2.Sin()).ApproximatelyEqualsTo(new Interval(-1.0, 1.0)));
            Assert.True((i3.Sin()).ApproximatelyEqualsTo(new Interval(Math.Sin(1.0), 1.0)));
            Assert.True((i6.Sin()).ApproximatelyEqualsTo(new Interval(-1.0, 0.0)));
        }

        [Fact]
        static void TestCos()
        {
            Assert.True((i1.Cos()).ApproximatelyEqualsTo(new Interval(Math.Cos(2.0), 1.0)));
            Assert.True((i2.Cos()).ApproximatelyEqualsTo(new Interval(-1.0, 1.0)));
            Assert.True((i3.Cos()).ApproximatelyEqualsTo(new Interval(Math.Cos(2.0), Math.Cos(1.0))));
            Assert.True((i6.Cos()).ApproximatelyEqualsTo(new Interval(Math.Cos(-2.0), 1.0)));
        }

        [Fact]
        static void TestAbs()
        {
            Assert.True((i1.Abs()).ApproximatelyEqualsTo(new Interval(0.0, 2.0)));
            Assert.True((i2.Abs()).ApproximatelyEqualsTo(new Interval(0.0, 4.0)));
            Assert.True((i3.Abs()).ApproximatelyEqualsTo(new Interval(1.0, 2.0)));
            Assert.True((i4.Abs()).ApproximatelyEqualsTo(new Interval(5.0, 5.1)));
            Assert.True((i5.Abs()).ApproximatelyEqualsTo(new Interval(5.0, 6.0)));
            Assert.True((i6.Abs()).ApproximatelyEqualsTo(new Interval(0.0, 2.0)));
            Assert.True((i7.Abs()).ApproximatelyEqualsTo(new Interval(0.0, 3.0)));
        }
        
        [Fact]
        static void TestExp()
        {
            Assert.True((i1.Exp()).ApproximatelyEqualsTo(new Interval(Math.Exp(-1.0), Math.Exp(2.0))));
            Assert.True((i2.Exp()).ApproximatelyEqualsTo(new Interval(Math.Exp(-4.0), Math.Exp(3.0))));
            Assert.True((i3.Exp()).ApproximatelyEqualsTo(new Interval(Math.Exp(1.0), Math.Exp(2.0))));
        }

        [Fact]
        static void TestSqrt()
        {
            Assert.True(i1.Sqrt().ApproximatelyEqualsTo(new Interval(0.0, Math.Sqrt(2.0))));
            Assert.True(i3.Sqrt().ApproximatelyEqualsTo(new Interval(Math.Sqrt(1.0), Math.Sqrt(2.0))));
            Assert.Throws<IntervalExceptions.BadAreaOperationException>(() => i5.Sqrt());
        }
        
        [Fact]
        static void TestLn()
        {
            Assert.True((i1.Ln()).ApproximatelyEqualsTo(new Interval(double.NegativeInfinity, Math.Log(2.0))));
            Assert.True((i2.Ln()).ApproximatelyEqualsTo(new Interval(double.NegativeInfinity, Math.Log(3.0))));
            Assert.True((i3.Ln()).ApproximatelyEqualsTo(new Interval(Math.Log(1.0), Math.Log(2.0))));
            Assert.True((i4.Ln()).ApproximatelyEqualsTo(new Interval(Math.Log(5.0), Math.Log(5.1))));
            Assert.Throws<IntervalExceptions.BadAreaOperationException>(() => i5.Ln());
            Assert.True((i6.Ln()).ApproximatelyEqualsTo(new Interval(double.NegativeInfinity, double.NegativeInfinity)));
            Assert.True((i7.Ln()).ApproximatelyEqualsTo(new Interval(double.NegativeInfinity, Math.Log(3.0))));
        }

        [Fact]
        static void TestMove()
        {
            Assert.True(i1.MoveBy(1.0) == i7);
            Assert.True(i7.MoveBy(-1.0) == i1);
            Assert.True(i5.MoveBy(0.5) == new Interval(-5.5, -4.5));
        }

        [Fact]
        static void TestRecover()
        {
            double min = -0.7, max = 1.5;
            Assert.True(i1.Constrain(min, max) == new Interval(min, max));
            Assert.True(i3.Constrain(min, max) == new Interval(1.0, max));
            Assert.True(i4.Constrain(min, max) == new Interval(max, max));
            Assert.True(i5.Constrain(min, max) == new Interval(min, min));
        }

        [Fact]
        static void TestSplitting()
        {
            Assert.True(i1.Bisect().Item1.ApproximatelyEqualsTo(new Interval(-1.0, 0.5)));
            Assert.True(i1.Bisect().Item2.ApproximatelyEqualsTo(new Interval(0.5, 2.0)));
            Assert.True(i1.Split(new [] {1, 2})[0].ApproximatelyEqualsTo(new Interval(-1.0, 0.0)));
            Assert.True(i1.Split(new [] {1, 2})[1].ApproximatelyEqualsTo(new Interval(0.0, 2.0)));
        }

        [Fact]
        static void TestJSON()
        {
            Assert.True(new Interval(i1.ConvertToJson()) == i1);
            Assert.True(new Interval(i2.ConvertToJson()) == i2);
            Assert.True(new Interval(i3.ConvertToJson()) == i3);
        }
        
    }
}