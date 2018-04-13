using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices.ComTypes;
using Newtonsoft.Json.Linq;
using OSOL.Extremum.Core.DotNet.Optimization;

namespace OSOL.Extremum.Core.DotNet.Vectors
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

        public sealed override Dictionary<string, double> Add(VectorObject<double> that) =>
            this.ElementWiseOp(that, (x, y) => x + y);

        public sealed override Dictionary<string, double> AddImputeMissingKeys(VectorObject<double> that) =>
            this.ElementWiseOpImputeMissingKeys(that, (x, y) => x + y, defaultValue: 0.0);

        public sealed override Dictionary<string, double> Multiply(double coefficient) =>
            this.Elements.ToDictionary(x => x.Key, x => coefficient * x.Value);

        public sealed override Dictionary<string, double> Multiply(VectorObject<double> that) =>
            this.ElementWiseOp(that, (x, y) => x * y);

        public sealed override Dictionary<string, double> MultiplyImputeMissingKeys(VectorObject<double> that) =>
            this.ElementWiseOpImputeMissingKeys(that, (x, y) => x * y, defaultValue: 1.0);

        public sealed override Dictionary<string, double> Subtract(VectorObject<double> that) =>
            this.ElementWiseOp(that, (x, y) => x - y);

        public sealed override Dictionary<string, double> SubtractImputeMissingKeys(VectorObject<double> that) =>
            this.ElementWiseOpImputeMissingKeys(that, (x, y) => x - y, defaultValue: 0.0);

        public RealVector MoveBy(Dictionary<string, double> delta) => this.AddImputeMissingKeys(new RealVector(delta));

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