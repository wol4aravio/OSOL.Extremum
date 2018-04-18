using System.Runtime.CompilerServices;
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
    }
    
}