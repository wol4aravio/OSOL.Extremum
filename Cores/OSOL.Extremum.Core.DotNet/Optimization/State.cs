using System;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;

namespace OSOL.Extremum.Core.DotNet.Optimization
{
    public class State<TBase, TFuncType, TV> where TV: class, IOptimizable<TBase, TFuncType>
    {
        public TV result = null;
        
        private Dictionary<string, object> parameters = new Dictionary<string, object>();

        public void SetParameter<T>(string name, T value)
        {
            parameters[name] = value;
        }

        public T GetParameter<T>(string name)
        {
            if (parameters.ContainsKey(name)) return (T) parameters[name];
            else throw new OptimizationExceptions.NoSuchParameterException(name);
        }

        public JObject ConvertToJson()
        {
            var result = new JObject();
            result["result"] = (this.result == null) ? new JObject("None") : this.result.ConvertToJson();
            var parameters = new JObject();
            var array = new JArray();
            foreach (var p in this.parameters)
            {
                JObject temp = new JObject();
                try
                {
                    var v = (TV) p.Value;
                    temp[p.Key] = v.ConvertToJson();
                }
                catch (Exception _)
                {
                    try
                    {
                        var v = (IEnumerable<TV>) p.Value;
                        var tempArray = new JArray();
                        foreach (var _v in v)
                            tempArray.Add(_v.ConvertToJson());
                        temp[p.Key] = tempArray;
                    }
                    catch (Exception __)
                    {
                        temp[p.Key] = new JObject(p.Value);
                    }
                }
                array.Add(temp);
            }
            result["parameters"] = array;
            return result;
        }
    }
}