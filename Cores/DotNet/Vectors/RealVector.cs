using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices.ComTypes;
using Newtonsoft.Json.Linq;
using OSOL.Extremum.Cores.DotNet.Optimization;

namespace OSOL.Extremum.Cores.DotNet.Vectors
{
    public class RealVector : VectorObject<double>, IOptimizable<RealVector, double>
    {
        public RealVector(Dictionary<string, double> elements)
        {
            this.Elements = elements;
        }

        public RealVector(JObject json)
        {
            Dictionary<string, double> elements = new Dictionary<string, double>();
            foreach (var j in (JArray) json["RealVector"]["elements"])
            {
                elements.Add(j["key"].Value<string>(), j["value"].Value<double>());
            }

            this.Elements = elements;
        }

        public static implicit operator RealVector(Dictionary<string, double> elements) => new RealVector(elements);

        public sealed override bool EqualsTo(VectorObject<double> that)
        {
            string[] keys_1 = this.Keys.ToArray();
            string[] keys_2 = that.Keys.ToArray();
            if (!(keys_1.All(k => keys_2.Contains(k)) && keys_2.All(k => keys_1.Contains(k))))
            {
                throw new VectorExceptions.DifferentKeysException(keys_1, keys_2);
            }
            else
            {
                return keys_1.All(k => this[k] == that[k]);
            }
        }

        public sealed override VectorObject<double> Add(VectorObject<double> that) =>
            new RealVector(this.ElementWiseOp(that, (x, y) => x + y));

        public sealed override VectorObject<double> AddImputeMissingKeys(VectorObject<double> that) =>
            new RealVector(this.ElementWiseOpImputeMissingKeys(that, (x, y) => x + y, defaultValue: 0.0));

        public sealed override VectorObject<double> Multiply(double coefficient) =>
            new RealVector(this.Elements.ToDictionary(x => x.Key, x => coefficient * x.Value));

        public sealed override VectorObject<double> Multiply(VectorObject<double> that) =>
            new RealVector(this.ElementWiseOp(that, (x, y) => x * y));

        public sealed override VectorObject<double> MultiplyImputeMissingKeys(VectorObject<double> that) =>
            new RealVector(this.ElementWiseOpImputeMissingKeys(that, (x, y) => x * y, defaultValue: 1.0));

        public sealed override VectorObject<double> Subtract(VectorObject<double> that) =>
            new RealVector(this.ElementWiseOp(that, (x, y) => x - y));

        public sealed override VectorObject<double> SubtractImputeMissingKeys(VectorObject<double> that) =>
            new RealVector(this.ElementWiseOpImputeMissingKeys(that, (x, y) => x - y, defaultValue: 0.0));

        public RealVector MoveBy(Dictionary<string, double> delta) => this.AddImputeMissingKeys(new RealVector(delta)).Elements;

        public RealVector Constrain(Dictionary<string, Tuple<double, double>> area)
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

                        double v = kvp.Value;
                        if (v > max)
                        {
                            return max;
                        }
                        else
                        {
                            if (v < min)
                            {
                                return min;
                            }

                            return v;
                        }
                    });
            return new RealVector(result);
        }

        public double GetPerformance(Func<Dictionary<string, double>, double> f) => f(this.Elements);

        public VectorObject<double> ToBasicForm() => this;

        public override VectorObject<double> Union(params Tuple<string, double>[] vectors)
        {
            var allKeys = new List<string>();
            allKeys.AddRange(this.Keys);
            allKeys.AddRange(vectors.Select(_ => _.Item1));
            allKeys = allKeys.Distinct().ToList();
            return new RealVector(allKeys.ToDictionary(k => k, k =>
            {
                var targetKey = vectors.Where(_ => _.Item1.Equals(k)).ToList();
                return targetKey.Count == 0 ? this[k] : targetKey.First().Item2;
            }));
        }

        public override Dictionary<string, double> DistanceFromArea(Dictionary<string, Tuple<double, double>> area)
        {
            return area.ToDictionary(kvp => kvp.Key, kvp =>
            {
                var min = kvp.Value.Item1;
                var max = kvp.Value.Item2;

                var v = this[kvp.Key];
                if (v < min) return min - v;
                else
                {
                    if (v > max) return v - max;
                    else return 0.0;
                }
            });
        }

        public JObject ConvertToJson()
        {
            JObject json = new JObject();
            json["RealVector"] = new JObject();
            JArray elements = new JArray();
            foreach (var kvp in this.Elements)
            {
                JObject temp = new JObject();
                temp["key"] = kvp.Key;
                temp["value"] = kvp.Value;
                elements.Add(temp);
            }

            json["RealVector"]["elements"] = elements;
            return json;
        }

    }

}