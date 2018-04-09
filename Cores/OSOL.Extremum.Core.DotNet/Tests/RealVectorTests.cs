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
        public void Keys()
        {
            Assert.True(v1.Keys.ToArray().Zip(new string[]{"x", "y", "z"}, (first, second) => first.Equals(second)).All(_ => _));
        }

//        [Fact]
//        public void ValueExtraction()
//        {
//            Assert.True(v1["x"] == 1.0);
//            Assert.True(v1["y"] == 2.0);
//            Assert.True(v1["z", 0.0] == 3.0);
//            Assert.True(v1["a", 0.0] == 0.0);
//            Assert.Throws<VectorExceptions.MissingKeyException>(() => v1["a"]);
//        }
        

    }
}