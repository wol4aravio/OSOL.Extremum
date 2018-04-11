using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json.Linq;
using OSOL.Extremum.Core.DotNet.Arithmetics;
using OSOL.Extremum.Core.DotNet.Optimization;

namespace OSOL.Extremum.Core.DotNet.Vectors
{
    public class IntervalVector: VectorObject<Interval>, IOptimizable<IntervalVector, Interval>
    {
        public IntervalVector(Dictionary<string, Interval> elements)
        {
            this.Elements = elements;
        }
        
        public IntervalVector(JObject json)
        {
            Dictionary<string, Interval> elements = new Dictionary<string, Interval>();
            foreach (var j in (JArray) json["IntervalVector"]["elements"])
                elements.Add(j["key"].Value<string>(), new Interval((JObject)j["value"]));
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

        public IntervalVector[] Split(double[] ratios, string key = null)
        {
            string splitKey = key ?? this.Elements.OrderBy(_ => -_.Value.Width).First().Key;
            var splitComponents = this[splitKey].Split(ratios);
            return splitComponents
                .Select(c =>
                {
                    var remaining = this.Elements
                        .Where(_ => !_.Key.Equals(splitKey));
                    remaining = remaining.Append(KeyValuePair.Create(splitKey, c));
                    return remaining;
                }).Select(v => new IntervalVector(v.ToDictionary(kvp => kvp.Key, kvp => kvp.Value)))
                .ToArray();
        }

        public Tuple<IntervalVector, IntervalVector> Bisect(string key = null)
        {
            var divided = this.Split(ratios: new double[] {1.0, 1.0}, key: key);
            return Tuple.Create(divided[0], divided[1]);
        }

        public IntervalVector MoveBy(Dictionary<string, double> delta) =>
            this.AddImputeMissingKeys(
                new IntervalVector(delta.ToDictionary(_ => _.Key, _ => new Interval(_.Value))));

        public IntervalVector Constrain(Dictionary<string, Tuple<double, double>> area)
        {
            var result = this.Elements
                .ToDictionary(
                    kvp => kvp.Key,
                    kvp =>
                    {
                        double min = double.NegativeInfinity, max = double.PositiveInfinity;
                        if (area.ContainsKey(kvp.Key))
                        {
                            min = area[kvp.Key].Item1;
                            max = area[kvp.Key].Item2;
                        }
                        return kvp.Value.Constrain(min, max);
                    });
            return new IntervalVector(result);
        }
        
        public double GetPerformance(Func<Dictionary<string, Interval>, Interval> f) => f(this.Elements).LowerBound;

        public VectorObject<double> ToBasicForm() =>
            new RealVector(this.Elements.ToDictionary(_ => _.Key, _ => _.Value.MiddlePoint));
        
        public JObject ConvertToJson()
        {
            JObject json = new JObject();
            json["IntervalVector"] = new JObject();
            JArray elements = new JArray();
            foreach (var kvp in this.Elements)
            {
                JObject temp = new JObject();
                temp["key"] = kvp.Key;
                temp["value"] = kvp.Value.ConvertToJson();
                elements.Add(temp);
            }
            json["IntervalVector"]["elements"] = elements;
            return json;
        }

    }
}