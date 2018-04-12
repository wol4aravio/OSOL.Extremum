using System;
using System.Collections.Generic;

namespace OSOL.Extremum.Core.DotNet.Optimization.Nodes
{
    
    using Area = Dictionary<string, Tuple<double, double>>;

    public class SetParametersNode<TBase, TFuncType, TV>: GeneralNode<TBase, TFuncType, TV>
        where TV: class, IOptimizable<TBase, TFuncType>
    {
        public Dictionary<string, object> Parameters;
        
        public SetParametersNode(int nodeId, Dictionary<string, object> parameters)
        {
            this.NodeId = nodeId;
            this.Parameters = parameters;
        }
        
        public override void Initialize(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area, State<TBase, TFuncType, TV> state)
        {
            foreach (var kvp in Parameters)
            {
                state.SetParameter(kvp.Key, kvp.Value);
            }
        }

        public override void Process(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area, State<TBase, TFuncType, TV> state)
        {
            // No action required
        }
    }
}