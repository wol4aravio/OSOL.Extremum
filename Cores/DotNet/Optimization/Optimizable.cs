using System;
using System.Collections.Generic;
using OSOL.Extremum.Cores.DotNet.Vectors;

using Newtonsoft.Json.Linq;

namespace OSOL.Extremum.Cores.DotNet.Optimization
{
    public interface IOptimizable<TBase, TFuncType>
    {
        TBase MoveBy(Dictionary<string, double> delta);

        TBase Constrain(Dictionary<string, Tuple<double, double>> area);

        Double GetPerformance(Func<Dictionary<string, TFuncType>, TFuncType> f);

        VectorObject<double> ToBasicForm();

        JObject ConvertToJson();
    }
}