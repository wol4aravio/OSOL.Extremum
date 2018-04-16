using System.Linq;
using Xunit;

using OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser;

namespace OSOL.Extremum.Core.DotNet.Tests
{
    public static class ParserTests
    {
        private static string str = "-x -+ 1.0 -- (sin(y) + cos(y)) * (exp(-x) + ln(10 + -y)) / (abs(-3.0) ^ sqrt(+4.0))";
        
        [Fact]
        public static void TestSplitToTokens()
        {
            var tokens = Parser.ToTokens(Parser.Prepare(str));
            var desiredTokens = new[]
            {
                "~", "x", "-", "1.0", "+", "(", "sin", "(", "y", ")", "+", "cos", "(", "y", ")", ")", "*", "(", "exp",
                "(", "~", "x", ")", "+", "ln", "(", "10", "-", "y", ")", ")", "/", "(", "abs", "(", "~", "3.0", ")",
                "^", "sqrt", "(", "4.0", ")", ")"
            };
            Assert.True(tokens.Zip(desiredTokens, (x, y) => x.Equals(y)).All(_ => _));
        }
    }
}