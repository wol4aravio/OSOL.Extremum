using System.Runtime.CompilerServices;
using OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser.Trees;
using OSOL.Extremum.Core.DotNet.Vectors;

namespace OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser.TreeFunctions
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
    }
    
}