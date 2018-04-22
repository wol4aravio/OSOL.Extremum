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
        
        public double Calculate(params RealVector[] vectors) => Tree.Calculate((RealVector)vectors.First().Union(vectors.Skip(1).ToArray()));

    }
    
}