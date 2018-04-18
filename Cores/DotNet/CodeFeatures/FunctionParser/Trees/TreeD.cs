using System;
using OSOL.Extremum.Cores.DotNet.Vectors;

namespace OSOL.Extremum.Cores.DotNet.CodeFeatures.FunctionParser.Trees
{
    public static class TreeD
    {
        public class AdditionTree : BinaryOpTree<double>
        {
            public AdditionTree(Tree<double> left, Tree<double> right)
            {
                this.Left = left;
                this.Right = right;
                this.Op = (x, y) => x + y;
            }
        }
        
        public class SubtractionTree : BinaryOpTree<double>
        {
            public SubtractionTree(Tree<double> left, Tree<double> right)
            {
                this.Left = left;
                this.Right = right;
                this.Op = (x, y) => x - y;
            }
        }
        
        public class MultiplicationTree : BinaryOpTree<double>
        {
            public MultiplicationTree(Tree<double> left, Tree<double> right)
            {
                this.Left = left;
                this.Right = right;
                this.Op = (x, y) => x * y;
            }
        }
        
        public class DivisionTree : BinaryOpTree<double>
        {
            public DivisionTree(Tree<double> left, Tree<double> right)
            {
                this.Left = left;
                this.Right = right;
                this.Op = (x, y) => x / y;
            }
        }
        
        public class PowerTree : BinaryOpTree<double>
        {
            public PowerTree(Tree<double> left, Tree<double> right)
            {
                this.Left = left;
                this.Right = right;
                this.Op = Math.Pow;
            }
        }

        public class NegTree : UnaryOpTree<double>
        {
            public NegTree(Tree<double> subTree)
            {
                this.SubTree = subTree;
                this.Op = x => -x;
            }
        }

        public class SinTree : UnaryOpTree<double>
        {
            public SinTree(Tree<double> subTree)
            {
                this.SubTree = subTree;
                this.Op = Math.Sin;
            }
        }

        public class CosTree : UnaryOpTree<double>
        {
            public CosTree(Tree<double> subTree)
            {
                this.SubTree = subTree;
                this.Op = Math.Cos;
            }
        }

        public class ExpTree : UnaryOpTree<double>
        {
            public ExpTree(Tree<double> subTree)
            {
                this.SubTree = subTree;
                this.Op = Math.Exp;
            }
        }

        public class AbsTree : UnaryOpTree<double>
        {
            public AbsTree(Tree<double> subTree)
            {
                this.SubTree = subTree;
                this.Op = Math.Abs;
            }
        }

        public class LnTree : UnaryOpTree<double>
        {
            public LnTree(Tree<double> subTree)
            {
                this.SubTree = subTree;
                this.Op = Math.Log;
            }
        }

        public class SqrtTree : UnaryOpTree<double>
        {
            public SqrtTree(Tree<double> subTree)
            {
                this.SubTree = subTree;
                this.Op = Math.Sqrt;
            }
        }

        public class ConstantTree : Tree<double>
        {
            public double Value;

            public ConstantTree(double value)
            {
                this.Value = value;
            }

            public override double Calculate(VectorObject<double> v) => Value;
        }

        public class VariableTree : Tree<double>
        {
            public string VarName;

            public VariableTree(string varName)
            {
                this.VarName = varName;
            }

            public override double Calculate(VectorObject<double> v) => v[VarName];
        }
    }
}