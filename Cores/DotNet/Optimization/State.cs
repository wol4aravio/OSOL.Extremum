using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json.Linq;

namespace OSOL.Extremum.Cores.DotNet.Optimization
{
    public class TypeSwitch
    {
        readonly Dictionary<Type, Action<object>> matches = new Dictionary<Type, Action<object>>();

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

        private readonly Dictionary<string, object> parameters = new Dictionary<string, object>();

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

        public JObject ConvertToJson(List<Func<object, JObject>> writers = null)
        {
            var json = new JObject();
            if (this.result == null)
                json.Add(new JProperty("result", new JValue("None")));
            else
                json["result"] = this.result.ConvertToJson();
            var array = new JArray();
            foreach (var p in this.parameters)
            {
                JObject temp = new JObject();
                var ts = new TypeSwitch();
                ts = ts
                    .Case((bool x) => temp[p.Key] = x)
                    .Case((double x) => temp[p.Key] = x)
                    .Case((int x) => temp[p.Key] = x)
                    .Case((DateTime x) => temp[p.Key] = x)
                    .Case((TV x) => temp[p.Key] = x.ConvertToJson())
                    .Case((Dictionary<string, double> d) => temp[p.Key] = new JArray(d))
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
                    .Case((object x) =>
                    {
                        if (writers != null)
                        {
                            var writerResults = writers.Select(w =>
                            {
                                try
                                {
                                    return w(x);
                                }
                                catch (Exception e)
                                {
                                    return null;
                                }
                            }).Where(_ => _ != null);
                            if (writerResults.Count() != 0)
                                temp[p.Key] = writerResults.First();
                            else
                            {
                                throw new Exception();
                            }
                        }
                        else
                        {
                            throw new Exception();
                        }
                    });

                ts.Switch(p.Value);

                array.Add(temp);
            }

            json["parameters"] = array;
            return json;
        }
    }
}