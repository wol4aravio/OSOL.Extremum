using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Cores.DotNet.Arithmetics;
using OSOL.Extremum.Cores.DotNet.CodeFeatures.FunctionParser.Trees;
using OSOL.Extremum.Cores.DotNet.Vectors;

namespace OSOL.Extremum.Cores.DotNet.CodeFeatures.FunctionParser.TreeFunctions
{
    public class IntervalTreeFunction
    {
        public Tree<Interval> Tree;
        
        public IntervalTreeFunction(Tree<Interval> tree)
        {
            this.Tree = tree;
        }
        
        public IntervalTreeFunction(string str) : this(Parser.BuildTreeI(Parser.ParseString(str)))
        {
            
        }

        public Interval Calculate(IntervalVector v) => Tree.Calculate(v);

        public Interval Calculate(params IntervalVector[] vectors)
        {
            var tail = vectors.Skip(1).Select(_ => _.Elements).ToArray();
            var elements = new List<Tuple<string, Interval>>();
            foreach (var e in tail)
            {
                elements.AddRange(e.Select(kvp => Tuple.Create(kvp.Key, kvp.Value)));
            }
            return Tree.Calculate((IntervalVector)vectors.First().Union(elements.ToArray()));
        }

    }
}