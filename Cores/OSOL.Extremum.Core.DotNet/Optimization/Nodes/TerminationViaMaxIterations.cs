using System;
using System.Collections.Generic;

namespace OSOL.Extremum.Core.DotNet.Optimization.Nodes
{
    public class TerminationViaMaxIterations<TBase, TFuncType, TV>: GeneralNode<TBase, TFuncType, TV>
        where TV: class, IOptimizable<TBase, TFuncType>
    {
        private string ParameterName;
        private int MaxIteration;

        public TerminationViaMaxIterations(int nodeId, int maxIteration, string parameterName = "currentIteration")
        {
            this.NodeId = nodeId;
            this.MaxIteration = maxIteration;
            this.ParameterName = parameterName;
        }

        public override void Initialize(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area, State<TBase, TFuncType, TV> state)
        {
            int? value = null;
            try
            {
                value = state.GetParameter<int>(ParameterName);
            }
            catch (OptimizationExceptions.NoSuchParameterException e)
            {
                state.SetParameter<int>(name: ParameterName, value: 0);
            }
            finally
            {
                if(value.HasValue) throw new OptimizationExceptions.ParameterAlreadyExistsException(ParameterName);
            }
        }

        public override void Process(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area, State<TBase, TFuncType, TV> state)
        {
            state.SetParameter(name: ParameterName, value: state.GetParameter<int>(ParameterName) + 1);
        }

        public override int? GetCurrentCondition(Func<Dictionary<string, TFuncType>, TFuncType> f, Area area, State<TBase, TFuncType, TV> state) => 
            state.GetParameter<int>(ParameterName) > MaxIteration ? 1 : 0;

    }
}