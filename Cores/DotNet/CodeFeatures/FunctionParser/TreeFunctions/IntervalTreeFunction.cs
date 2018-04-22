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

        public Interval Calculate(params IntervalVector[] vectors) => Tree.Calculate((IntervalVector)vectors.First().Union(vectors.Skip(1).ToArray()));

    }
}