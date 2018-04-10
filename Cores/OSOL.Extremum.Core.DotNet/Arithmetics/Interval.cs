using System;
using System.Linq;
using System.Net.Sockets;
using System.Reflection.Metadata.Ecma335;

namespace OSOL.Extremum.Core.DotNet.Arithmetics
{
    public struct Interval
    {
        public static double MinWidth = 1e-5;
        
        public double LowerBound, UpperBound;
        public double MiddlePoint => 0.5 * (UpperBound + LowerBound);
        public double Width => UpperBound - LowerBound;
        public double Radius => 0.5 * Width;

        public Interval(double value)
        {
            this.LowerBound = this.UpperBound = value;
        }
        public Interval(double lowerBound, double upperBound)
        {
            double w = upperBound - lowerBound;
            if (w < MinWidth)
            {
                this.LowerBound = this.UpperBound = 0.5 *(lowerBound + upperBound);
            }
            else
            {
                this.LowerBound = lowerBound;
                this.UpperBound = upperBound;
            }
        }
        
        public static implicit operator Interval(double value) => new Interval(value);

        public override string ToString() => $"[{LowerBound}; {UpperBound}]";

        public bool EqualsTo(Interval that) => this.LowerBound == that.LowerBound && this.UpperBound == that.UpperBound;

        public static bool operator ==(Interval a, Interval b) => a.EqualsTo(b);
        public static bool operator !=(Interval a, Interval b) => !(a == b);

        public bool ApproximatelyEqualsTo(Interval that, double maxError = 1e-5)
        {
            Func<double, double, double> getDifference = (a, b) =>
            {
                double delta = Math.Abs(b - a);
                if (double.IsNaN(delta)) return a == b ? 0.0 : 1.0;
                else return delta;
            };
            double errorLeft = getDifference(this.LowerBound, that.LowerBound);
            double errorRight = getDifference(this.UpperBound, that.UpperBound);
            return errorLeft + errorRight <= maxError;
        }
        
        public Interval Neg() => new Interval(-UpperBound, -LowerBound);
        public static Interval operator -(Interval i) => i.Neg();
        
        public Interval Add(Interval that) => new Interval(this.LowerBound + that.LowerBound, this.UpperBound + that.UpperBound);
        public static Interval operator +(Interval a, Interval b) => a.Add(b);

        public Interval Subtract(Interval that) => this.Add(that.Neg());
        public static Interval operator -(Interval a, Interval b) => a.Subtract(b);

        public Interval Multiply(Interval that)
        {
            double[] values = new double[]
            {
                this.LowerBound * that.LowerBound,
                this.LowerBound * that.UpperBound,
                this.UpperBound * that.LowerBound,
                this.UpperBound * that.UpperBound
            };
            return new Interval(values.Min(), values.Max());
        }
        public static Interval operator *(Interval a, Interval b) => a.Multiply(b);

        public Interval Divide(Interval that)
        {
            if (that.LowerBound > 0.0 || that.UpperBound < 0.0)
                return this.Multiply(new Interval(1.0 / that.UpperBound, 1.0 / that.LowerBound));
            if (that.LowerBound == 0.0)
                return this.Multiply(new Interval(1.0 / that.UpperBound, double.PositiveInfinity));
            if (that.UpperBound == 0.0)
                return this.Multiply(new Interval(double.NegativeInfinity, 1 / that.LowerBound));
            return new Interval(double.NegativeInfinity, double.PositiveInfinity);
        }
        public static Interval operator /(Interval a, Interval b) => a.Divide(b);

        public Interval Power(Interval that)
        {
            if(that.Width > 0) throw new IntervalExceptions.UnknownOperationException("[a; b] ^ [c; d] for (d - c) > 0");
            else
            {
                int powerIndex = (int)that.MiddlePoint;
                double v1 = Math.Pow(this.LowerBound, powerIndex);
                double v2 = Math.Pow(this.UpperBound, powerIndex);
                if(powerIndex % 2 == 1)
                    return new Interval(v1, v2);
                else
                {
                    if(this.LowerBound * this.UpperBound < 0) return new Interval(0.0, Math.Max(v1, v2));
                    else return this.LowerBound >= 0 ? new Interval(v1, v2) : new Interval(v2, v1);
                }
            }
        }

        public Interval Abs()
        {
            double v1 = Math.Abs(this.LowerBound);
            double v2 = Math.Abs(this.UpperBound);
            if(this.LowerBound * this.UpperBound < 0) return new Interval(0.0, Math.Max(v1, v2));
            else return this.LowerBound >= 0 ? new Interval(v1, v2) : new Interval(v2, v1);
        }
        
        public Interval Sin()
        {
            if (this.Width > Math.PI * 2.0)
                return new Interval(-1, 1);
            double val, k, r_l = Math.Sin(this.LowerBound), r_u = Math.Sin(this.UpperBound);
            if (r_u < r_l)
            {
                k = r_l;
                r_l = r_u;
                r_u = k;
            }
            k = (int)(this.LowerBound / (Math.PI / 2.0));
            val = k * (Math.PI / 2.0);
            while (val < this.LowerBound)
            {
                ++k;
                val = k * (Math.PI / 2.0);
            }
            for (; val <= this.UpperBound; ++k, val = k * (Math.PI / 2.0))
            {
                if (r_l == -1 && r_u == 1)
                    break;
                else
                {
                    if (Math.Sin(val) == -1)
                    {
                        r_l = -1;
                        continue;
                    }
                    if (Math.Sin(val) == 1)
                    {
                        r_u = 1;
                        continue;
                    }
                }
            }
            return new Interval(r_l, r_u);
        }

        public Interval Cos()
        {
            if (this.Width > Math.PI * 2.0)
                return new Interval(-1, 1);
            double val, k, r_l = Math.Cos(this.LowerBound), r_u = Math.Cos(this.UpperBound);
            if (r_u < r_l)
            {
                k = r_l;
                r_l = r_u;
                r_u = k;
            }
            k = (int)(this.LowerBound / (Math.PI / 2.0));
            val = k * (Math.PI / 2.0);
            while (val < this.LowerBound)
            {
                ++k;
                val = k * (Math.PI / 2.0);
            }
            for (; val <= this.UpperBound; ++k, val = k * (Math.PI / 2.0))
            {
                if (r_l == -1 && r_u == 1)
                    break;
                else
                {
                    switch (Math.Cos(val))
                    {
                        case -1:
                            r_l = -1;
                            continue;
                        case 1:
                            r_u = 1;
                            continue;
                    }
                }
            }
            return new Interval(r_l, r_u);
        }

        public Interval Exp() => new Interval(Math.Exp(this.LowerBound), Math.Exp(this.UpperBound));

        public Interval Sqrt()
        {
            if (this.UpperBound < 0)
                throw new IntervalExceptions.BadAreaOperationException(opName: "Ln", interval: this);
            else
            {
                if (this.LowerBound < 0) return new Interval(0.0, Math.Sqrt(this.UpperBound));
                else return new Interval(Math.Sqrt(this.LowerBound), Math.Sqrt(this.UpperBound));
            }  
        }

        public Interval Ln()
        {
            if (this.UpperBound < 0)
                throw new IntervalExceptions.BadAreaOperationException(opName: "Ln", interval: this);
            else
            {
                if (this.LowerBound < 0) return new Interval(double.NegativeInfinity, Math.Log(this.UpperBound));
                else return new Interval(Math.Log(this.LowerBound), Math.Log(this.UpperBound));
            }  
        }
        
    }
}