using System;
using System.Collections.Generic;
using System.Linq;

namespace OSOL.Extremum.Core.DotNet.Vectors
{
    public abstract class VectorObject<TBase>
    {
        public Dictionary<string, TBase> Elements;

        public IEnumerable<string> Keys => this.Elements.Keys;
        
        public TBase this[string key]
        {
            get
            {
                try { return this.Elements[key]; }
                catch(Exception e) { throw new VectorExceptions.MissingKeyException(key); }
            }
        set => Elements[key] = value;
        }

        public TBase this[string key, TBase defaultValue] => Keys.Contains(key) ? this[key] : defaultValue;
            
        public override string ToString() =>
            string.Join(separator: "\n", values: Elements.Select(x => $"{x.Key} -> {x.Value.ToString()}"));

        public Dictionary<string, TBase> ElementWiseOp(VectorObject<TBase> that, Func<TBase, TBase, TBase> op)
        {
            string[] keys_1 = this.Keys.ToArray();
            string[] keys_2 = that.Keys.ToArray();
            if (!(keys_1.All(k => keys_2.Contains(k)) && keys_2.All(k => keys_1.Contains(k))))
                throw new VectorExceptions.DifferentKeysException(keys_1, keys_2);
            else return keys_1.ToDictionary(k => k, k => op(this[k], that[k]));
        }
        
        public Dictionary<string, TBase> ElementWiseOpImputeMissingKeys(VectorObject<TBase> that, Func<TBase, TBase, TBase> op, TBase defaultValue)
        {
            List<string> mergedKeys = new List<string>(this.Keys);
            foreach (string k in that.Keys)
                if(!mergedKeys.Contains(k)) mergedKeys.Add(k);
            return mergedKeys.ToDictionary(k => k, k => op(this[k, defaultValue], that[k, defaultValue]));
        }

        public abstract bool EqualsTo(VectorObject<TBase> that);
        public static bool operator ==(VectorObject<TBase> a, VectorObject<TBase> b) => a.EqualsTo(b);
        public static bool operator !=(VectorObject<TBase> a, VectorObject<TBase> b) => !(a == b);

        public abstract Dictionary<string, TBase> Add(VectorObject<TBase> that);
        public static Dictionary<string, TBase> operator +(VectorObject<TBase> a, VectorObject<TBase> b) => a.Add(b);
        
        public abstract Dictionary<string, TBase> AddImputeMissingKeys(VectorObject<TBase> that);
        
        public abstract Dictionary<string, TBase> Multiply(double coefficient);
        public static Dictionary<string, TBase> operator *(VectorObject<TBase> a, double coefficient) => a.Multiply(coefficient);

        private Dictionary<string, TBase> Neg() => Multiply(coefficient: -1.0);
        public static Dictionary<string, TBase> operator -(VectorObject<TBase> a) => a.Neg();

        public abstract Dictionary<string, TBase> Subtract(VectorObject<TBase> that);
        public static Dictionary<string, TBase> operator -(VectorObject<TBase> a, VectorObject<TBase> b) => a.Subtract(b);
        public abstract Dictionary<string, TBase> SubtractImputeMissingKeys(VectorObject<TBase> that);
        
        public abstract Dictionary<string, TBase> Multiply(VectorObject<TBase> that);
        public static Dictionary<string, TBase> operator *(VectorObject<TBase> a, VectorObject<TBase> b) => a.Multiply(b);
        public abstract Dictionary<string, TBase> MultiplyImputeMissingKeys(VectorObject<TBase> that);

    }
}