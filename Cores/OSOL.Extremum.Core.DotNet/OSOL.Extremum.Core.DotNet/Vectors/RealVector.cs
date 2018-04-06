using System.Collections.Generic;
using System.Linq;

namespace OSOL.Extremum.Core.DotNet.Vectors
{
    public class RealVector: VectorObject<double>
    {

        public RealVector(Dictionary<string, double> elements)
        {
            this.Elements = elements;
        }
        
        public static implicit operator RealVector(Dictionary<string, double> elements) => new RealVector(elements);
                
        public sealed override bool EqualsTo(VectorObject<double> that)
        {
            string[] keys_1 = this.Keys.ToArray();
            string[] keys_2 = that.Keys.ToArray();
            if (!(keys_1.All(k => keys_2.Contains(k)) || keys_2.All(k => keys_1.Contains(k))))
                throw new VectorExceptions.DifferentKeysException(keys_1, keys_2);
            else return keys_1.All(k => this[k] == that[k]);
        }

        public sealed override Dictionary<string, double> Add(VectorObject<double> that) =>
            this.ElementWiseOp(that, (x, y) => x + y).ToDictionary(p => p.Item1, p => p.Item2);
        public sealed override Dictionary<string, double> AddImputeMissingKeys(VectorObject<double> that) =>
            this.ElementWiseOpImputeMissingKeys(that, (x, y) => x + y, defaultValue: 0.0).ToDictionary(p => p.Item1, p => p.Item2);

        public sealed override Dictionary<string, double> Multiply(double coefficient) =>
            this.Elements.Select(x => (x.Key, coefficient * x.Value)).ToDictionary(x => x.Item1, x => x.Item2);
        
        public sealed override Dictionary<string, double> Multiply(VectorObject<double> that) =>
            this.ElementWiseOp(that, (x, y) => x * y).ToDictionary(p => p.Item1, p => p.Item2);
        public sealed override Dictionary<string, double> MultiplyImputeMissingKeys(VectorObject<double> that) =>
            this.ElementWiseOpImputeMissingKeys(that, (x, y) => x * y, defaultValue: 1.0).ToDictionary(p => p.Item1, p => p.Item2);
   
        public sealed override Dictionary<string, double> Subtract(VectorObject<double> that) =>
            this.ElementWiseOp(that, (x, y) => x - y).ToDictionary(p => p.Item1, p => p.Item2);
        public sealed override Dictionary<string, double> SubtractImputeMissingKeys(VectorObject<double> that) =>
            this.ElementWiseOpImputeMissingKeys(that, (x, y) => x - y, defaultValue: 0.0).ToDictionary(p => p.Item1, p => p.Item2);
    }
    
}