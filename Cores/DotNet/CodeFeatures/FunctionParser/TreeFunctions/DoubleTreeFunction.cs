using System;
using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Cores.DotNet.CodeFeatures.FunctionParser.Trees;
using OSOL.Extremum.Cores.DotNet.Vectors;

namespace OSOL.Extremum.Cores.DotNet.CodeFeatures.FunctionParser.TreeFunctions
{
    public class DoubleTreeFunction
    {
        public Tree<double> Tree;
        
        public DoubleTreeFunction(Tree<double> tree)
        {
            this.Tree = tree;
        }

        public DoubleTreeFunction(string str) : this(Parser.BuildTreeD(Parser.ParseString(str)))
        {
            
        }

        public double Calculate(RealVector v) => Tree.Calculate(v);

        public double Calculate(params RealVector[] vectors)
        {
            var tail = vectors.Skip(1).Select(_ => _.Elements).ToArray();
            var elements = new List<Tuple<string, double>>();
            foreach (var e in tail)
            {
                elements.AddRange(e.Select(kvp => Tuple.Create(kvp.Key, kvp.Value)));
            }
            return Tree.Calculate((RealVector)vectors.First().Union(elements.ToArray()));
        } 

    }
    
}