using System;
using System.Runtime.CompilerServices;
using OSOL.Extremum.Core.DotNet.Arithmetics;
using OSOL.Extremum.Core.DotNet.Vectors;

namespace OSOL.Extremum.Core.DotNet.CodeFeatures.FunctionParser.Trees
{
    public static class TreeI
    {
        public class AdditionTree : BinaryOpTree<Interval>
        {
            public AdditionTree(Tree<Interval> left, Tree<Interval> right)
            {
                this.Left = left;
                this.Right = right;
                this.Op = (x, y) => x + y;
            }
        }
        
        public class SubtractionTree : BinaryOpTree<Interval>
        {
            public SubtractionTree(Tree<Interval> left, Tree<Interval> right)
            {
                this.Left = left;
                this.Right = right;
                this.Op = (x, y) => x - y;
            }
        }
        
        public class MultiplicationTree : BinaryOpTree<Interval>
        {
            public MultiplicationTree(Tree<Interval> left, Tree<Interval> right)
            {
                this.Left = left;
                this.Right = right;
                this.Op = (x, y) => x * y;
            }
        }
        
        public class DivisionTree : BinaryOpTree<Interval>
        {
            public DivisionTree(Tree<Interval> left, Tree<Interval> right)
            {
                this.Left = left;
                this.Right = right;
                this.Op = (x, y) => x / y;
            }
        }
        
        public class PowerTree : BinaryOpTree<Interval>
        {
            public PowerTree(Tree<Interval> left, Tree<Interval> right)
            {
                this.Left = left;
                this.Right = right;
                this.Op = (x, y) => x.Power(y);
            }
        }

        public class NegTree : UnaryOpTree<Interval>
        {
            public NegTree(Tree<Interval> subTree)
            {
                this.SubTree = subTree;
                this.Op = x => x.Neg();
            }
        }

        public class SinTree : UnaryOpTree<Interval>
        {
            public SinTree(Tree<Interval> subTree)
            {
                this.SubTree = subTree;
                this.Op = x => x.Sin();
            }
        }

        public class CosTree : UnaryOpTree<Interval>
        {
            public CosTree(Tree<Interval> subTree)
            {
                this.SubTree = subTree;
                this.Op = x => x.Cos();
            }
        }

        public class ExpTree : UnaryOpTree<Interval>
        {
            public ExpTree(Tree<Interval> subTree)
            {
                this.SubTree = subTree;
                this.Op = x => x.Exp();
            }
        }

        public class AbsTree : UnaryOpTree<Interval>
        {
            public AbsTree(Tree<Interval> subTree)
            {
                this.SubTree = subTree;
                this.Op = x => x.Abs();
            }
        }

        public class LnTree : UnaryOpTree<Interval>
        {
            public LnTree(Tree<Interval> subTree)
            {
                this.SubTree = subTree;
                this.Op = x => x.Ln();
            }
        }

        public class SqrtTree : UnaryOpTree<Interval>
        {
            public SqrtTree(Tree<Interval> subTree)
            {
                this.SubTree = subTree;
                this.Op = x => x.Sqrt();
            }
        }
        
        public class ConstantTree : Tree<Interval>
        {
            public Interval Value;

            public ConstantTree(Interval value)
            {
                this.Value = value;
            }

            public override Interval Calculate(VectorObject<Interval> v) => Value;
        }

        public class VariableTree : Tree<Interval>
        {
            public string VarName;

            public VariableTree(string varName)
            {
                this.VarName = varName;
            }

            public override Interval Calculate(VectorObject<Interval> v) => v[VarName];
        }
    }
}