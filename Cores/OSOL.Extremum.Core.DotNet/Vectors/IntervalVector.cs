using System.Collections.Generic;
using System.Linq;
using OSOL.Extremum.Core.DotNet.Arithmetics;

namespace OSOL.Extremum.Core.DotNet.Vectors
{
    public class IntervalVector: VectorObject<Interval>
    {
        public IntervalVector(Dictionary<string, Interval> elements)
        {
            this.Elements = elements;
        }
        
        public static implicit operator IntervalVector(Dictionary<string, Interval> elements) => new IntervalVector(elements);
                
        public sealed override bool EqualsTo(VectorObject<Interval> that)
        {
            string[] keys_1 = this.Keys.ToArray();
            string[] keys_2 = that.Keys.ToArray();
            if (!(keys_1.All(k => keys_2.Contains(k)) && keys_2.All(k => keys_1.Contains(k))))
                throw new VectorExceptions.DifferentKeysException(keys_1, keys_2);
            else return keys_1.All(k => this[k] == that[k]);
        }

        public sealed override Dictionary<string, Interval> Add(VectorObject<Interval> that) =>
            this.ElementWiseOp(that, (x, y) => x + y);
        public sealed override Dictionary<string, Interval> AddImputeMissingKeys(VectorObject<Interval> that) =>
            this.ElementWiseOpImputeMissingKeys(that, (x, y) => x + y, defaultValue: 0.0);

        public sealed override Dictionary<string, Interval> Multiply(double coefficient) =>
            this.Elements.Select(x => (x.Key, coefficient * x.Value)).ToDictionary(x => x.Item1, x => x.Item2);
        
        public sealed override Dictionary<string, Interval> Multiply(VectorObject<Interval> that) =>
            this.ElementWiseOp(that, (x, y) => x * y);
        public sealed override Dictionary<string, Interval> MultiplyImputeMissingKeys(VectorObject<Interval> that) =>
            this.ElementWiseOpImputeMissingKeys(that, (x, y) => x * y, defaultValue: 1.0);
   
        public sealed override Dictionary<string, Interval> Subtract(VectorObject<Interval> that) =>
            this.ElementWiseOp(that, (x, y) => x - y);
        public sealed override Dictionary<string, Interval> SubtractImputeMissingKeys(VectorObject<Interval> that) =>
            this.ElementWiseOpImputeMissingKeys(that, (x, y) => x - y, defaultValue: 0.0);
    }
}