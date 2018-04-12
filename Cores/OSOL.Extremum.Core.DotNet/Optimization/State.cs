using System;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;

namespace OSOL.Extremum.Core.DotNet.Optimization
{
    public class TypeSwitch
    {
        Dictionary<Type, Action<object>> matches = new Dictionary<Type, Action<object>>();

        public TypeSwitch Case<T>(Action<T> action)
        {
            matches.Add(typeof(T), (x) => action((T) x));
            return this;
        }

        public void Switch(object x)
        {
            matches[x.GetType()](x);
        }
    }

    public class State<TBase, TFuncType, TV> where TV : class, IOptimizable<TBase, TFuncType>
    {
        public TV result = null;

        private Dictionary<string, object> parameters = new Dictionary<string, object>();

        public void SetParameter<T>(string name, T value)
        {
            parameters[name] = value;
        }

        public T GetParameter<T>(string name)
        {
            if (parameters.ContainsKey(name))
            {
                return (T) parameters[name];
            }
            else
            {
                throw new OptimizationExceptions.NoSuchParameterException(name);
            }
        }

        public JObject ConvertToJson()
        {
            var json = new JObject();
            json["result"] = (this.result == null) ? new JObject("None") : this.result.ConvertToJson();
            var array = new JArray();
            foreach (var p in this.parameters)
            {
                JObject temp = new JObject();
                var ts = new TypeSwitch()
                    .Case((bool x) => temp[p.Key] = x)
                    .Case((double x) => temp[p.Key] = x)
                    .Case((int x) => temp[p.Key] = x)
                    .Case((DateTime x) => temp[p.Key] = x)
                    .Case((TV x) => temp[p.Key] = x.ConvertToJson())
                    .Case((TV[] x) =>
                    {
                        var v = (IEnumerable<TV>) p.Value;
                        var tempArray = new JArray();
                        foreach (var _v in v)
                        {
                            tempArray.Add(_v.ConvertToJson());
                        }

                        temp[p.Key] = tempArray;
                    })
                    .Case((List<TV> x) =>
                    {
                        var v = (IEnumerable<TV>) p.Value;
                        var tempArray = new JArray();
                        foreach (var _v in v)
                        {
                            tempArray.Add(_v.ConvertToJson());
                        }

                        temp[p.Key] = tempArray;
                    })
                    .Case((object x) => throw new Exception());

                ts.Switch(p.Value);

                array.Add(temp);
            }

            json["parameters"] = array;
            return json;
        }
    }
}