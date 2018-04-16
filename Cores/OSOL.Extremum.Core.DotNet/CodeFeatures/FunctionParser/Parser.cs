using System;
using System.Linq;
using System.Text.RegularExpressions;

namespace OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser
{
    public static class Parser
    {
        private static Tuple<string, string> space = Tuple.Create(" ", "");
        private static Tuple<string, string> doubleMinus = Tuple.Create("\\-\\-", "+");
        private static Tuple<string, string> plusMinus = Tuple.Create("\\+\\-", "-");
        private static Tuple<string, string> minusPlus = Tuple.Create("\\-\\+", "-");
        private static Tuple<string, string> inTheBeginning = Tuple.Create("^\\-", "~");
        private static Tuple<string, string> afterOpeningBracket = Tuple.Create("\\(\\-", "(~");
        private static Tuple<string, string> unnecessaryAddition = Tuple.Create("\\(\\+", "(");
        
        private static string tokenRegex = "(?<=[-+{*}/{)~(}^])|(?=[-+{*}/{)~(}^])";
        
        private static Tuple<string, string>[] rules = new[]
        {
            space,
            doubleMinus,
            plusMinus,
            minusPlus,
            inTheBeginning,
            afterOpeningBracket,
            unnecessaryAddition
        };

        public static string Prepare(string str) =>
            rules.Aggregate(str, (f, rule) => Regex.Replace(f, rule.Item1, rule.Item2));

        public static string[] ToTokens(string str) => Regex.Split(str, tokenRegex).Where(_ => _.Length > 0).ToArray();
//
//        def toTokens(str: String): Seq[String] =
//        str.split(tokenRegex)

    }
}