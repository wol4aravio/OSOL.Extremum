using System;
using OSOL.Extremum.Core.DotNet.Vectors;

namespace OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser.Trees
{
    public abstract class Tree<T>
    {
        public abstract T Calculate(VectorObject<T> v);
    }

    public abstract class BinaryOpTree<T> : Tree<T>
    {
        public Tree<T> Left, Right;
        public Func<T, T, T> Op;

        public override T Calculate(VectorObject<T> v) => Op(Left.Calculate(v), Right.Calculate(v));
    }
    
    public abstract class UnaryOpTree<T> : Tree<T>
    {
        public Tree<T> SubTree;
        public Func<T, T> Op;

        public override T Calculate(VectorObject<T> v) => Op(SubTree.Calculate(v));
    }

    
}