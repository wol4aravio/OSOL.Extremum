using System;
using System.Collections.Generic;

namespace OSOL.Extremum.Core.DotNet.Optimization.Nodes
{
    public class TerminationViaMaxTime<TBase, TFuncType, TV>: GeneralNode<TBase, TFuncType, TV>
        where TV: class, IOptimizable<TBase, TFuncType>
    {
        private string ParameterName;
        private double MaxTime;

        public TerminationViaMaxTime(int nodeId, double maxTime, string parameterName = "startTime")
        {
            this.NodeId = nodeId;
            this.MaxTime = maxTime;
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
                state.SetParameter<DateTime>(name: ParameterName, value: DateTime.Now);
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
            (DateTime.Now - state.GetParameter<DateTime>(ParameterName)).TotalSeconds > MaxTime ? 1 : 0;

    }
}