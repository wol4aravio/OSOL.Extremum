using OSOL.Extremum.Core.DotNet.Arithmetics;
using OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser.Trees;
using OSOL.Extremum.Core.DotNet.Vectors;

namespace OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser.TreeFunctions
{
    public class IntervalTreeFunction
    {
        public Tree<Interval> Tree;
        
        public IntervalTreeFunction(Tree<Interval> tree)
        {
            this.Tree = tree;
        }

        public Interval Calculate(IntervalVector v) => Tree.Calculate(v);
    }
}