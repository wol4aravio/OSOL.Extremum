using Xunit;

using OSOL.Extremum.Core.DotNet.Arithmetics;

namespace OSOL.Extremum.Core.DotNet.Tests
{
    public class IntervalTests
    {
        Interval i1 = new Interval(-1.0, 2.0);
        Interval i2 = new Interval(-4.0, 3.0);
        Interval i3 = new Interval(1.0, 2.0);
        Interval i4 = new Interval(5.0, 5.1);
        Interval i5 = new Interval(-6.0, -5.0);
        Interval i6 = new Interval(-2.0, 0.0);
        Interval i7 = new Interval(0.0, 3.0);

        [Fact]
        void TestToString()
        {
            Assert.True(i1.ToString().Equals("[-1; 2]"));
            Assert.True(i4.ToString().Equals("[5; 5.1]"));
            Assert.True(i7.ToString().Equals("[0; 3]"));
        }

        [Fact]
        void TestMiddlePoint()
        {
            Assert.Equal(i1.MiddlePoint, 0.5);
            Assert.Equal(i3.MiddlePoint, 1.5);
            Assert.Equal(i7.MiddlePoint, 1.5);
        }

        [Fact]
        void TestWidth()
        {
            Assert.Equal(i1.Width, 3.0);
            Assert.Equal(i3.Width, 1.0);
            Assert.Equal(i7.Width, 3.0);
        }
    }
}