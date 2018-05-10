using System;
using System.Linq;
using Newtonsoft.Json.Linq;

namespace OSOL.Extremum.Cores.DotNet.Arithmetics
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
            this.LowerBound = value;
            this.UpperBound = value;
        }

        public Interval(JObject json)
        {
            this.LowerBound = json["Interval"]["lower_bound"].Value<double>();
            this.UpperBound = json["Interval"]["upper_bound"].Value<double>();
        }

        public Interval(double lowerBound, double upperBound)
        {
            if (lowerBound > upperBound)
            {
                throw new IntervalExceptions.MinMaxFailureException(lowerBound, upperBound);
            }

            double w = upperBound - lowerBound;
            if (w < MinWidth)
            {
                this.LowerBound = 0.5 * (lowerBound + upperBound);
                this.UpperBound = 0.5 * (lowerBound + upperBound);
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
                if (double.IsNaN(delta))
                {
                    return a == b ? 0.0 : 1.0;
                }
                else
                {
                    return delta;
                }
            };
            double errorLeft = getDifference(this.LowerBound, that.LowerBound);
            double errorRight = getDifference(this.UpperBound, that.UpperBound);
            return errorLeft + errorRight <= maxError;
        }

        public Interval Neg() => new Interval(-UpperBound, -LowerBound);
        public static Interval operator -(Interval i) => i.Neg();

        public Interval Add(Interval that) =>
            new Interval(this.LowerBound + that.LowerBound, this.UpperBound + that.UpperBound);

        public static Interval operator +(Interval a, Interval b) => a.Add(b);

        public Interval Subtract(Interval that) => this.Add(that.Neg());
        public static Interval operator -(Interval a, Interval b) => a.Subtract(b);

        public Interval Multiply(Interval that)
        {
            var values = new []
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
            {
                return this.Multiply(new Interval(1.0 / that.UpperBound, 1.0 / that.LowerBound));
            }

            if (that.LowerBound == 0.0)
            {
                return this.Multiply(new Interval(1.0 / that.UpperBound, double.PositiveInfinity));
            }

            if (that.UpperBound == 0.0)
            {
                return this.Multiply(new Interval(double.NegativeInfinity, 1 / that.LowerBound));
            }

            return new Interval(double.NegativeInfinity, double.PositiveInfinity);
        }

        public static Interval operator /(Interval a, Interval b) => a.Divide(b);

        public Interval MoveBy(double delta) => this.Add(delta);

        public Interval Constrain(double min, double max)
        {
            Func<double, double> check = v =>
            {
                if (v < min)
                {
                    return min;
                }
                else
                {
                    if (v > max)
                    {
                        return max;
                    }
                    else
                    {
                        return v;
                    }
                }
            };
            return new Interval(check(this.LowerBound), check(this.UpperBound));
        }

        public Interval[] Split(double[] ratios)
        {
            double sum = ratios.Sum();
            double last = this.LowerBound;
            Interval[] result = new Interval[ratios.Length];
            for (int i = 0; i < result.Length; ++i)
            {
                result[i] = new Interval(last, last + ratios[i] * this.Width / sum);
                last = result[i].UpperBound;
            }

            return result;
        }

        public Tuple<Interval, Interval> Bisect()
        {
            var divided = this.Split(new [] {1.0, 1.0});
            return Tuple.Create(divided[0], divided[1]);
        }

        public JObject ConvertToJson()
        {
            JObject json = new JObject();
            JObject interval = new JObject();
            interval["lower_bound"] = this.LowerBound;
            interval["upper_bound"] = this.UpperBound;
            json["Interval"] = interval;
            return json;
        }

    }
}