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
            get => this.Elements[key];
            set => Elements[key] = value;
        }

        public TBase this[string key, TBase defaultValue]
        {
            get => Keys.Contains(key) ? this[key] : defaultValue;
            set => throw new Exception("This indexer is used only for accessing elements");
        }

        public override string ToString() =>
            string.Join(separator: "\n", values: Elements.Select(x => $"{x.Key} -> {x.Value.ToString()}"));

        public IEnumerable<Tuple<String, TBase>> ElementWiseOp(VectorObject<TBase> that, Func<Tuple<TBase, TBase>, TBase> op)
        {
            string[] keys_1 = this.Keys.ToArray();
            string[] keys_2 = that.Keys.ToArray();
            if (!(keys_1.All(k => keys_2.Contains(k)) || keys_2.All(k => keys_1.Contains(k))))
                throw new VectorExceptions.DifferentKeysException(keys_1, keys_2);
            else return keys_1.Select(k => Tuple.Create(k, op(Tuple.Create(this[k], that[k]))));
        }
        
        public IEnumerable<Tuple<String, TBase>> ElementWiseOpImputeMissingKeys(VectorObject<TBase> that, Func<Tuple<TBase, TBase>, TBase> op, TBase defaultValue)
        {
            List<string> mergedKeys = new List<string>(this.Keys);
            foreach (string k in that.Keys)
                if(!mergedKeys.Contains(k)) mergedKeys.Add(k);
            return mergedKeys.Select(k => Tuple.Create(k, op(Tuple.Create(this[k, defaultValue], that[k, defaultValue]))));
        }

        public abstract bool EqualsTo(VectorObject<TBase> that);
        public static bool operator ==(VectorObject<TBase> a, VectorObject<TBase> b) => a.EqualsTo(b);
        public static bool operator !=(VectorObject<TBase> a, VectorObject<TBase> b) => !(a == b);

        public abstract VectorObject<TBase> Add(VectorObject<TBase> that);
        public static VectorObject<TBase> operator +(VectorObject<TBase> a, VectorObject<TBase> b) => a.Add(b);
        
        public abstract VectorObject<TBase> AddImputeMissingKeys(VectorObject<TBase> that, TBase defaultValue);
        
        public abstract VectorObject<TBase> Multiply(double coefficient);
        public static VectorObject<TBase> operator *(VectorObject<TBase> a, double coefficient) => a.Multiply(coefficient);

        public VectorObject<TBase> Neg() => this.Multiply(coefficient: -1.0);
        public static VectorObject<TBase> operator -(VectorObject<TBase> a) => a.Neg();

        public VectorObject<TBase> Subtract(VectorObject<TBase> that) => this.Add(that.Neg());
        public static VectorObject<TBase> operator -(VectorObject<TBase> a, VectorObject<TBase> b) => a.Subtract(b);
        
        public abstract VectorObject<TBase> SubtractImputeMissingKeys(VectorObject<TBase> that, TBase defaultValue);
        
        public abstract VectorObject<TBase> Multiply(VectorObject<TBase> that);
        public static VectorObject<TBase> operator *(VectorObject<TBase> a, VectorObject<TBase> b) => a.Multiply(b);
        
        public abstract VectorObject<TBase> MultiplyImputeMissingKeys(VectorObject<TBase> that, TBase defaultValue);

    }
}